# Feature-map normalization lab

This isolated lab documents the display transformation used by Sprint 2 without
changing inference or any registered artifact.

For each selected channel, the API keeps the raw minimum, maximum, mean and
standard deviation. It then maps only that channel to `[0, 1]`:

```text
display = (activation - raw_min) / (raw_max - raw_min)
```

If the channel is constant, every display value is `0`. Because each channel
has its own scale, colors may be compared spatially inside one map but not as
absolute activation magnitudes between different maps. Raw statistics remain
the auditable evidence for magnitude comparisons.

The production implementation is
`ai-services/cnn-feature-map-viewer/src/cnn_feature_map_viewer/service.py`.
