"""Controlled forward-hook lifecycle for allowlisted CNN representations."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from types import TracebackType

import torch
from torch import nn
from torch.utils.hooks import RemovableHandle

from cnn_feature_map_viewer.model import FashionCnn


class ActivationCapture:
    """Capture selected outputs and always remove registered hooks."""

    def __init__(self, model: FashionCnn, layer_names: Iterable[str]) -> None:
        available = model.observable_layers
        requested = tuple(dict.fromkeys(layer_names))
        unknown = set(requested).difference(available)
        if unknown:
            raise ValueError(f"Unknown observable layer: {sorted(unknown)[0]}")
        self._modules = {name: available[name] for name in requested}
        self._handles: list[RemovableHandle] = []
        self.outputs: dict[str, torch.Tensor] = {}

    def __enter__(self) -> ActivationCapture:
        for name, module in self._modules.items():
            self._handles.append(module.register_forward_hook(self._hook(name)))
        return self

    def __exit__(
        self,
        _: type[BaseException] | None,
        __: BaseException | None,
        ___: TracebackType | None,
    ) -> None:
        for handle in self._handles:
            handle.remove()
        self._handles.clear()

    def _hook(
        self,
        name: str,
    ) -> Callable[[nn.Module, tuple[torch.Tensor, ...], torch.Tensor], None]:
        def capture(_: nn.Module, __: tuple[torch.Tensor, ...], output: torch.Tensor) -> None:
            self.outputs[name] = output.detach().cpu().clone()

        return capture


def run_with_activations(
    model: FashionCnn,
    inputs: torch.Tensor,
    layer_names: Iterable[str],
) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
    with ActivationCapture(model, layer_names) as capture:
        logits = model(inputs)
    return logits, capture.outputs
