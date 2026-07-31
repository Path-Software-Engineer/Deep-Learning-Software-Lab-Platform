---
name: Axon Deep Learning Visual Lab
description: Dark scientific interface for inspecting registered PyTorch evidence across three educational modules.
framework: Next.js 16
language: TypeScript
styling: CSS Modules
---

# Axon Design System

## Product character

Axon is an evidence-first technical lab. The interface should feel precise,
quiet and exploratory: scientific instrumentation rather than a marketing
dashboard. It must never imply that an activation, latent coordinate or smooth
interpolation is a causal explanation.

## Visual foundation

| Token | Value | Use |
|---|---|---|
| Canvas | `#07090f` | primary background |
| Surface | `#0d111a` | navigation and large panels |
| Raised | `#121724` | cards, controls and inspectors |
| Hairline | `rgba(183, 193, 220, 0.16)` | borders and separators |
| Text | `#f6f5fb` | headings and primary values |
| Muted | `#9299a9` | descriptions and metadata |
| Quiet | `#656d7e` | secondary labels |
| Violet | `#9d82ff` | neural and latent emphasis |
| Cyan | `#59d5f7` | computed evidence and focus |
| Mint | `#66ddb1` | connected and healthy state |
| Danger | `#ff6d7b` | controlled failure state |

Use `Manrope` for interface text and `DM Mono` for versions, coordinates,
tensor shapes and machine-generated evidence. Avoid ornamental gradients except
for one restrained violet-to-cyan emphasis in a hero or active visualization.

## Layout

- Fixed desktop sidebar: `248px`.
- Main content maximum: `1500px`.
- Base spacing rhythm: `8px`.
- Card radius: `13px` to `18px`.
- Borders: one pixel; shadows remain subtle and local.
- Desktop content may use asymmetric 7/5 or 2/1 grids.
- Collapse secondary grids below `1180px`.
- Convert the sidebar into a compact top navigation below `820px`.
- Use a single column and reduced padding below `560px`.

## Components

### Platform navigation

Show all three modules in the same order: Neural Trace, Feature Maps and Latent
Space. The active module receives a tinted surface, visible border and
`aria-current="page"`. Never hide unfinished or unavailable state behind a
working-looking link.

### Evidence card

An evidence card contains an uppercase mono eyebrow, one prominent value, a
short unit or scope statement and optional provenance. Values returned by the
API may be formatted but not recomputed.

### Scientific visualization

SVG and image panels must retain readable labels, a textual interpretation and
keyboard-equivalent controls. Color is supplementary; state also uses shape,
border, text or `aria-*`.

### Boundary panel

Every module ends with a visible evidence boundary. Use numbered statements and
plain language. Keep the boundary adjacent to the evidence it qualifies.

### Loading and failure

Loading announces progress through `aria-live`. Errors use a stable alert
panel, human-readable reason and explicit Retry action. Never replace failed
model evidence with invented values.

## Interaction

- Minimum interactive target: `44 × 44px`.
- Use `:focus-visible` with a two-pixel cyan outline and offset.
- Support pointer, Enter and Space for custom SVG targets.
- Animation duration: `120–240ms`; movement is subtle and transform-based.
- Under `prefers-reduced-motion: reduce`, remove decorative animation and
  preserve state changes without motion.
- Disable controls only while their request is genuinely active.

## Content rules

- Prefer “registered checkpoint”, “held-out evidence”, “reference label” and
  “display transformation”.
- Do not use “understands”, “explains why”, “semantic truth” or “production
  ready” for model internals.
- Surface dataset size, split, model version and limitations close to the
  relevant output.

## Screen mapping

- `/` — XOR Neural Network Explainer: signal trace and training evidence.
- `/cnn` — CNN Feature Map Viewer: prediction, layer selection and controlled
  activation maps.
- `/autoencoder` — Autoencoder Latent Space Demo: source/reconstruction,
  registered 2D points, neighbors and decoder-backed interpolation.
