from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest
from autoencoder_latent_space import (
    AutoencoderLatentSpace,
    AutoencoderRequestError,
)


@pytest.fixture
def latent_space(
    autoencoder_artifact_directory: Path,
) -> AutoencoderLatentSpace:
    return AutoencoderLatentSpace(autoencoder_artifact_directory)


def test_summary_publishes_model_metrics_and_boundaries(
    latent_space: AutoencoderLatentSpace,
) -> None:
    summary = latent_space.summary()

    assert summary["schema_version"] == "1.0"
    assert summary["module"] == "autoencoder-latent-space-demo"
    assert summary["model"]["parameter_count"] == 215_923
    assert summary["model"]["latent_shape"] == [2]
    assert summary["evaluation"]["samples"] == 150
    assert summary["evaluation"]["mean_squared_error"] < 0.05
    assert summary["latent_contract"]["reference_points"] == 100
    assert len(summary["limitations"]) >= 4


def test_samples_publish_one_representative_per_class(
    latent_space: AutoencoderLatentSpace,
) -> None:
    resource = latent_space.samples()

    assert len(resource["samples"]) == 10
    assert {sample["label_index"] for sample in resource["samples"]} == set(range(10))
    assert all(
        sample["image_data_uri"].startswith("data:image/png;base64,")
        for sample in resource["samples"]
    )


def test_latent_points_include_coordinates_labels_and_images(
    latent_space: AutoencoderLatentSpace,
) -> None:
    resource = latent_space.latent_points()

    assert len(resource["points"]) == 100
    assert all(len(point["coordinate"]) == 2 for point in resource["points"])
    assert set(resource["bounds"]) == {"x", "y"}
    assert "registered" in resource["interpretation"]


def test_reconstruction_and_neighbors_are_generated_by_service(
    latent_space: AutoencoderLatentSpace,
) -> None:
    resource = latent_space.reconstruct("latent-08-00")

    assert resource["sample"]["label"] == "Bag"
    assert len(resource["latent_coordinate"]) == 2
    assert resource["reconstruction"]["mean_squared_error"] >= 0
    assert resource["reconstruction"]["image_data_uri"].startswith(
        "data:image/png;base64,"
    )
    assert len(resource["neighbors"]) == 5
    assert all(neighbor["distance"] >= 0 for neighbor in resource["neighbors"])


def test_interpolation_uses_real_decoder_and_includes_endpoints(
    latent_space: AutoencoderLatentSpace,
) -> None:
    resource = latent_space.interpolate(
        start_id="latent-01-00",
        end_id="latent-09-00",
        steps=7,
    )

    assert resource["start"]["id"] == "latent-01-00"
    assert resource["end"]["id"] == "latent-09-00"
    assert len(resource["steps"]) == 7
    assert resource["steps"][0]["alpha"] == 0.0
    assert resource["steps"][-1]["alpha"] == 1.0
    assert all(
        step["image_data_uri"].startswith("data:image/png;base64,")
        for step in resource["steps"]
    )


@pytest.mark.parametrize(
    ("operation", "code"),
    [
        (lambda service: service.reconstruct("unknown"), "unknown_latent_point"),
        (
            lambda service: service.interpolate(
                start_id="latent-01-00",
                end_id="latent-01-00",
                steps=7,
            ),
            "identical_interpolation_endpoints",
        ),
        (
            lambda service: service.interpolate(
                start_id="latent-01-00",
                end_id="latent-02-00",
                steps=99,
            ),
            "invalid_interpolation_steps",
        ),
    ],
)
def test_invalid_requests_fail_with_stable_codes(
    latent_space: AutoencoderLatentSpace,
    operation: Callable[[AutoencoderLatentSpace], object],
    code: str,
) -> None:
    with pytest.raises(AutoencoderRequestError) as error:
        operation(latent_space)

    assert error.value.code == code
