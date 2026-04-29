# Running App-Builder AI On Windows

This repo has two services:

- Backend API: `http://127.0.0.1:8100`
- Frontend console: `http://127.0.0.1:5173`

## Backend

If Python is installed globally:

```powershell
cd D:\App-Builder-AI\backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn app_builder_ai.main:app --host 127.0.0.1 --port 8100
```

If PowerShell blocks activation scripts, use the full `.venv\Scripts\python.exe` command shown above instead of activating the environment.

## Frontend

Use `npm.cmd` on Windows if PowerShell blocks `npm.ps1`:

```powershell
cd D:\App-Builder-AI\frontend
npm.cmd install
npm.cmd run dev -- --host 127.0.0.1 --port 5173
```

## Verified Commands

```powershell
cd D:\App-Builder-AI\backend
.\.venv\Scripts\python.exe -m pytest

cd D:\App-Builder-AI\frontend
npm.cmd run build
```
