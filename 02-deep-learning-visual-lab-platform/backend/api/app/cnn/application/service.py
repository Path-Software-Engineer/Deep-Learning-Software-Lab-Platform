"""Typed use-case boundary around the registered CNN engine."""

from __future__ import annotations

from cnn_feature_map_viewer import CnnFeatureMapViewer

from app.cnn.interfaces.resources import (
    CnnFeatureMapsResource,
    CnnPredictionResource,
    CnnSamplesResource,
    CnnSummaryResource,
)


class CnnApplicationService:
    def __init__(self, viewer: CnnFeatureMapViewer) -> None:
        self._viewer = viewer

    def get_summary(self) -> CnnSummaryResource:
        return CnnSummaryResource.model_validate(self._viewer.summary())

    def get_samples(self) -> CnnSamplesResource:
        return CnnSamplesResource.model_validate(self._viewer.samples())

    def predict(
        self,
        *,
        sample_id: str | None,
        image_bytes: bytes | None,
        media_type: str | None,
    ) -> CnnPredictionResource:
        return CnnPredictionResource.model_validate(
            self._viewer.predict(
                sample_id=sample_id,
                image_bytes=image_bytes,
                media_type=media_type,
            )
        )

    def get_feature_maps(
        self,
        *,
        sample_id: str | None,
        image_bytes: bytes | None,
        media_type: str | None,
        layer: str,
        channels: tuple[int, ...],
    ) -> CnnFeatureMapsResource:
        return CnnFeatureMapsResource.model_validate(
            self._viewer.feature_maps(
                sample_id=sample_id,
                image_bytes=image_bytes,
                media_type=media_type,
                layer=layer,
                channels=channels,
            )
        )
