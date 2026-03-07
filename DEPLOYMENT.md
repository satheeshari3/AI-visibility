# Deploying AI Rank

The app serves both the frontend and API from a single FastAPI process. Set `OPENAI_API_KEY` in your host's environment.

## Render (recommended, free tier)

1. Go to [render.com](https://render.com) and sign in
2. **New** → **Web Service**
3. Connect your GitHub repo: `satheeshari3/AI-visibility`
4. Render will auto-detect `render.yaml` — no extra config needed
5. Add environment variable: `OPENAI_API_KEY` = your key
6. Click **Create Web Service**

You’ll get a URL like `ai-rank.onrender.com`.

## Railway

1. Go to [railway.app](https://railway.app) and sign in
2. **New Project** → **Deploy from GitHub repo**
3. Select `satheeshari3/AI-visibility`
4. Add variable: `OPENAI_API_KEY` = your key
5. Deploy (start command is in `railway.json`)

## Fly.io

1. Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/): `brew install flyctl`
2. Log in: `fly auth login`
3. From the project folder: `fly launch` (use existing fly.toml)
4. Set secret: `fly secrets set OPENAI_API_KEY=your_key`
5. Deploy: `fly deploy`

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
