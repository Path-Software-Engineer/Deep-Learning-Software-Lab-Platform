# Docker execution profile

The final project runs as two explicit containers because the production
responsibilities remain separate:

- `api`: FastAPI plus the three registered PyTorch engines and their immutable
  checkpoints.
- `web`: the standalone Next.js application. Its `/api/*` rewrite targets the
  internal `api` service.

No database, queue or object store is required by the three educational,
read-only modules.

## Start

```powershell
docker compose up --build --detach
docker compose ps
```

Open:

- Web platform: `http://127.0.0.1:3000`
- Autoencoder module: `http://127.0.0.1:3000/autoencoder`
- API documentation: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Verify

```powershell
docker compose ps
docker compose logs --tail 80 api web
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-WebRequest http://127.0.0.1:3000/autoencoder -UseBasicParsing
```

Do not treat `running` as equivalent to `healthy`; both health checks must pass.

## Stop

```powershell
docker compose down
```

The containers do not hold persistent user data. Model evidence is built into
the API image from integrity-checked repository artifacts.
