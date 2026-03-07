# Deploying AI Rank

## Quick deploy (Railway / Render / Fly.io)

The app serves both the frontend and API from a single FastAPI process. Set `OPENAI_API_KEY` in your host's environment.

### Railway

1. Connect your repo at [railway.app](https://railway.app)
2. Add `OPENAI_API_KEY` in Variables
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Deploy

### Render

1. New Web Service → connect repo
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add `OPENAI_API_KEY` in Environment

### Fly.io

1. Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/)
2. Run `fly launch` in the project directory
3. Set secret: `fly secrets set OPENAI_API_KEY=your_key`
4. Deploy: `fly deploy`

Create `fly.toml` if needed:

```toml
app = "ai-rank"

[env]
  PORT = "8080"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  processes = ["app"]
  min_machines_running = 0

[[vm]]
  memory = "512mb"
  cpu_kind = "shared"
  cpus = 1
```

Start command: `uvicorn main:app --host 0.0.0.0 --port 8080`

## Environment variables

| Variable        | Required | Description              |
|----------------|----------|--------------------------|
| `OPENAI_API_KEY` | Yes    | Your OpenAI API key      |
| `PORT`         | No       | Port (default 8000)      |

## Local production test

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Then open http://localhost:8000
