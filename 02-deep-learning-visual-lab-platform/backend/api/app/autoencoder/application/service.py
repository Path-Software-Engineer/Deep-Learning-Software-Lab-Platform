"""Typed use-case boundary around the registered autoencoder engine."""

from __future__ import annotations

from autoencoder_latent_space import AutoencoderLatentSpace

from app.autoencoder.interfaces.resources import (
    AutoencoderInterpolationResource,
    AutoencoderLatentPointsResource,
    AutoencoderReconstructionResource,
    AutoencoderSamplesResource,
    AutoencoderSummaryResource,
)


class AutoencoderApplicationService:
    def __init__(self, latent_space: AutoencoderLatentSpace) -> None:
        self._latent_space = latent_space

    def get_summary(self) -> AutoencoderSummaryResource:
        return AutoencoderSummaryResource.model_validate(
            self._latent_space.summary()
        )

    def get_samples(self) -> AutoencoderSamplesResource:
        return AutoencoderSamplesResource.model_validate(
            self._latent_space.samples()
        )

    def get_latent_points(self) -> AutoencoderLatentPointsResource:
        return AutoencoderLatentPointsResource.model_validate(
            self._latent_space.latent_points()
        )

    def reconstruct(self, point_id: str) -> AutoencoderReconstructionResource:
        return AutoencoderReconstructionResource.model_validate(
            self._latent_space.reconstruct(point_id)
        )

    def interpolate(
        self,
        *,
        start_id: str,
        end_id: str,
        steps: int,
    ) -> AutoencoderInterpolationResource:
        return AutoencoderInterpolationResource.model_validate(
            self._latent_space.interpolate(
                start_id=start_id,
                end_id=end_id,
                steps=steps,
            )
        )
