from __future__ import annotations

import pytest
from neural_network_explainer.dataset import validate_xor_inputs, xor_target, xor_tensors


def test_xor_tensors_preserve_the_controlled_truth_table() -> None:
    features, targets = xor_tensors()
    assert features.shape == (4, 2)
    assert targets.shape == (4, 1)
    assert targets.reshape(-1).tolist() == [0.0, 1.0, 1.0, 0.0]


@pytest.mark.parametrize(
    ("inputs", "expected"),
    [((0.0, 0.0), 0), ((0.0, 1.0), 1), ((1.0, 0.0), 1), ((1.0, 1.0), 0)],
)
def test_xor_target_matches_the_truth_table(
    inputs: tuple[float, float],
    expected: int,
) -> None:
    assert xor_target(inputs) == expected


def test_invalid_xor_input_is_rejected() -> None:
    with pytest.raises(ValueError, match="must be 0 or 1"):
        validate_xor_inputs((0.5, 1.0))
