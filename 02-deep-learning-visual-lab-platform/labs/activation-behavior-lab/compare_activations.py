"""Isolated comparison; intentionally not imported by production."""

from __future__ import annotations

import json

import torch


def main() -> None:
    values = torch.tensor([-4.0, -1.0, 0.0, 1.0, 4.0])
    result = {
        "preactivations": values.tolist(),
        "tanh": torch.tanh(values).tolist(),
        "sigmoid": torch.sigmoid(values).tolist(),
        "relu": torch.relu(values).tolist(),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
