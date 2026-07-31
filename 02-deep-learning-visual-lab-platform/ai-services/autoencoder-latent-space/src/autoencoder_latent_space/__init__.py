"""Public boundary for the registered autoencoder representation module."""

from autoencoder_latent_space.artifacts import (
    AutoencoderArtifactIntegrityError,
)
from autoencoder_latent_space.service import (
    AutoencoderLatentSpace,
    AutoencoderRequestError,
)

__all__ = [
    "AutoencoderArtifactIntegrityError",
    "AutoencoderLatentSpace",
    "AutoencoderRequestError",
]
