from __future__ import annotations

from pathlib import Path

import pytest
from cnn_feature_map_viewer import CnnFeatureMapViewer, CnnRequestError


@pytest.fixture
def viewer(cnn_artifact_directory: Path) -> CnnFeatureMapViewer:
    return CnnFeatureMapViewer(cnn_artifact_directory)


def test_summary_publishes_model_layers_and_evaluation(
    viewer: CnnFeatureMapViewer,
) -> None:
    summary = viewer.summary()

    assert summary["schema_version"] == "1.0"
    assert summary["module"] == "cnn-feature-map-viewer"
    assert summary["model"]["parameter_count"] == 207_018
    assert [layer["id"] for layer in summary["layers"]] == [
        "block1_relu",
        "block2_relu",
    ]
    assert summary["evaluation"]["samples"] == 150
    assert summary["evaluation"]["accuracy"] > 0.75


def test_samples_publish_one_bounded_image_per_class(
    viewer: CnnFeatureMapViewer,
) -> None:
    resource = viewer.samples()

    assert len(resource["samples"]) == 10
    assert {sample["label_index"] for sample in resource["samples"]} == set(range(10))
    assert all(
        sample["image_data_uri"].startswith("data:image/png;base64,")
        for sample in resource["samples"]
    )


def test_prediction_returns_class_confidence_and_probabilities(
    viewer: CnnFeatureMapViewer,
) -> None:
    resource = viewer.predict(sample_id="fashion-08")

    assert resource["input"]["registered_label"] == "Bag"
    assert resource["prediction"]["predicted_class"] == "Bag"
    assert 0 <= resource["prediction"]["confidence"] <= 1
    assert len(resource["prediction"]["probabilities"]) == 10


def test_feature_maps_preserve_raw_metadata_and_bounded_display_values(
    viewer: CnnFeatureMapViewer,
) -> None:
    resource = viewer.feature_maps(
        sample_id="fashion-09",
        layer="block2_relu",
        channels=(0, 3, 7),
    )

    representation = resource["representation"]
    assert representation["activation_tensor_shape"] == [1, 32, 14, 14]
    assert len(representation["maps"]) == 3
    for feature_map in representation["maps"]:
        assert feature_map["tensor_shape"] == [1, 32, 14, 14]
        assert feature_map["map_shape"] == [14, 14]
        flattened = [value for row in feature_map["values"] for value in row]
        assert min(flattened) >= 0
        assert max(flattened) <= 1
        assert feature_map["raw_max"] >= feature_map["raw_min"]


@pytest.mark.parametrize(
    ("kwargs", "code"),
    [
        ({"sample_id": "unknown"}, "invalid_sample"),
        (
            {
                "sample_id": "fashion-00",
                "layer": "unknown",
                "channels": (0,),
            },
            "invalid_layer",
        ),
        (
            {
                "sample_id": "fashion-00",
                "layer": "block1_relu",
                "channels": (16,),
            },
            "invalid_channel",
        ),
        (
            {
                "sample_id": "fashion-00",
                "layer": "block1_relu",
                "channels": (0, 0),
            },
            "duplicate_channel",
        ),
    ],
)
def test_invalid_requests_fail_with_stable_codes(
    viewer: CnnFeatureMapViewer,
    kwargs: dict[str, object],
    code: str,
) -> None:
    method = viewer.feature_maps if "layer" in kwargs else viewer.predict
    with pytest.raises(CnnRequestError) as error:
        method(**kwargs)

    assert error.value.code == code
