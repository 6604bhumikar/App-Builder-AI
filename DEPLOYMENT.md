# Deployment Guide

Use GitHub as the source for both deployments:

- Frontend: Vercel
- Backend API: Render

## 1. Deploy Backend On Render

1. Open Render and create a new Blueprint or Web Service from this GitHub repo.
2. If using Blueprint, Render will read `render.yaml` from the repo root.
3. If creating the service manually, use:
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app_builder_ai.main:app --host 0.0.0.0 --port $PORT`
   - Health check path: `/health`
4. After deploy, copy the backend URL, for example:

```text
https://app-builder-ai-api.onrender.com
```

## 2. Deploy Frontend On Vercel

1. Import the same GitHub repo into Vercel.
2. Set the project root directory to:

```text
frontend
```

3. Vercel should use the included `frontend/vercel.json`.
4. Add this environment variable in Vercel project settings:

```text
VITE_API_BASE_URL=https://your-render-backend-url.onrender.com
```

5. Deploy.

## 3. Verify

Open the Vercel URL and generate a project. The UI should call:

```text
https://your-render-backend-url.onrender.com/api/projects/generate
```

You can also check the backend directly:

```text
https://your-render-backend-url.onrender.com/health
```

## Notes

- Vercel is best for the Vite React frontend.
- Render is better for the FastAPI backend because the API runs as a persistent Python web service.
- The current backend stores project history in memory, so history resets when the backend restarts.
