# Activation Behavior Lab

## Nemesis question

How do `tanh`, `sigmoid`, and `ReLU` transform the same controlled
preactivations, and what cannot be inferred from those values?

## Boundary

This lab is isolated from production code. It does not produce or replace the
official XOR checkpoint. Its purpose is to compare activation ranges and
saturation behavior with controlled inputs.

## Reproduce

```powershell
python .\labs\activation-behavior-lab\compare_activations.py
```

## Conclusion

`tanh` preserves sign and maps values to `[-1, 1]`; `sigmoid` maps values to
`[0, 1]`; `ReLU` removes negative values. A larger activation is not evidence
that a neuron is more important, nor is any activation a causal explanation.
