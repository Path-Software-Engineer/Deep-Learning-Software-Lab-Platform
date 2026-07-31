# Sprint 3 Visual Validation

## Runtime evidence

The production Next.js build and FastAPI service were started locally on
`127.0.0.1`. The following real HTTP checks passed:

- `GET /`, `GET /cnn` and `GET /autoencoder`: `200 text/html`;
- `GET /health`: `200 application/json`;
- `GET /api/v1/autoencoder/summary`: `200`;
- `GET /api/v1/autoencoder/latent-points`: `200`;
- same-origin Next.js proxy to the autoencoder summary: `200`;
- reconstruction of `latent-08-00`: `Bag`, five neighbors;
- seven-step interpolation: alpha `0.0` through `1.0`.

## Browser boundary

The connected browser explicitly rejected navigation to
`http://127.0.0.1:3000` under its security policy. The policy also prohibited
switching to Chrome, raw CDP or another Playwright surface to obtain the same
result.

Therefore desktop 1440 px, tablet 768 px and mobile 390 px screenshots were not
captured in this run. No mockups or substituted screenshots were created.
Console, visual overflow, keyboard navigation and reduced-motion behavior
remain pending a browser session in which this local URL is permitted.

## Static evidence

- frontend lint, strict TypeScript and component tests passed;
- the Next.js production build generated `/`, `/cnn` and `/autoencoder`;
- responsive breakpoints, visible focus and reduced-motion rules are versioned
  in the CSS Modules and `.stitch/DESIGN.md`;
- the Playwright Sprint 3 scenario is versioned but was not executed as a
  workaround for the browser policy.
