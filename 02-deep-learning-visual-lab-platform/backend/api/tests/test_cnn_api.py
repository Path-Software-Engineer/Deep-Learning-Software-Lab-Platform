from __future__ import annotations

import io

from fastapi.testclient import TestClient
from PIL import Image


def _png() -> bytes:
    image = Image.new("L", (32, 48), color=160)
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return stream.getvalue()


def test_cnn_summary_and_samples_are_published(client: TestClient) -> None:
    summary = client.get("/api/v1/cnn/summary")
    samples = client.get("/api/v1/cnn/samples")

    assert summary.status_code == 200
    assert summary.json()["model"]["version"] == "fashion-cnn-v1"
    assert summary.json()["evaluation"]["samples"] == 150
    assert samples.status_code == 200
    assert len(samples.json()["samples"]) == 10


def test_registered_sample_prediction_is_read_only(client: TestClient) -> None:
    response = client.post("/api/v1/cnn/predict?sample_id=fashion-08")

    assert response.status_code == 200
    assert response.json()["input"]["registered_label"] == "Bag"
    assert response.json()["prediction"]["predicted_class"] == "Bag"


def test_uploaded_png_is_validated_and_predicted(client: TestClient) -> None:
    response = client.post(
        "/api/v1/cnn/predict",
        content=_png(),
        headers={"Content-Type": "image/png"},
    )

    assert response.status_code == 200
    assert response.json()["input"]["source"] == "upload"
    assert response.json()["input"]["original_shape"] == [48, 32]
    assert len(response.json()["prediction"]["probabilities"]) == 10


def test_feature_map_contract_preserves_shapes_and_raw_statistics(
    client: TestClient,
) -> None:
    response = client.post(
        "/api/v1/cnn/feature-maps"
        "?sample_id=fashion-09"
        "&layer=block2_relu"
        "&channels=0&channels=3&channels=7"
    )

    assert response.status_code == 200
    resource = response.json()
    assert resource["representation"]["activation_tensor_shape"] == [1, 32, 14, 14]
    assert [feature_map["channel"] for feature_map in resource["representation"]["maps"]] == [
        0,
        3,
        7,
    ]


def test_invalid_image_and_layer_use_stable_error_envelopes(
    client: TestClient,
) -> None:
    invalid_image = client.post(
        "/api/v1/cnn/predict",
        content=b"invalid",
        headers={"Content-Type": "image/png"},
    )
    invalid_layer = client.post(
        "/api/v1/cnn/feature-maps?sample_id=fashion-00&layer=unknown&channels=0"
    )

    assert invalid_image.status_code == 422
    assert invalid_image.json()["error"]["code"] == "invalid_image"
    assert invalid_layer.status_code == 422
    assert invalid_layer.json()["error"]["code"] == "invalid_layer"


def test_missing_input_and_wrong_media_type_fail_closed(client: TestClient) -> None:
    missing = client.post("/api/v1/cnn/predict")
    wrong_media = client.post(
        "/api/v1/cnn/predict",
        content=_png(),
        headers={"Content-Type": "application/octet-stream"},
    )

    assert missing.status_code == 422
    assert missing.json()["error"]["code"] == "missing_input"
    assert wrong_media.status_code == 422
    assert wrong_media.json()["error"]["code"] == "unsupported_media_type"
