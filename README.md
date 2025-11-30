# Personal Finance Tracker — Setup & Run

This repository contains a Streamlit-based personal finance tracker (`aap.py`). To run it and resolve editor diagnostics, follow the steps below.

## Setup

1. Install dependencies from `requirements.txt` using the Python interpreter you use for this workspace.

Example (Windows PowerShell, Anaconda recommended):

```powershell
# Example using Anaconda Python
"C:/ProgramData/Anaconda3/python.exe" -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt

# Or run with the global Anaconda interpreter directly:
"C:/ProgramData/Anaconda3/python.exe" -m pip install -r requirements.txt
```

If you use Python 3.13 and `pip install` fails to compile packages like `pandas`, prefer Python 3.11 or use conda/mamba as described below.

## Recommended: install with mamba/conda (Windows)

```powershell
mamba create -n finance-tracker python=3.11 -y
mamba activate finance-tracker
python -m pip install -r requirements.txt
```

## Running locally

Start the app using the interpreter with the installed packages:

```powershell
# Using Anaconda python
"C:/ProgramData/Anaconda3/python.exe" -m streamlit run aap.py --server.port 8501 --server.address 0.0.0.0
```

Open http://127.0.0.1:8501 in your browser to view the app.

## Troubleshooting: Editor/Pylance warnings

- If you still see `Import "streamlit" could not be resolved`, ensure you selected the same Python interpreter as above in VS Code (Command Palette → Python: Select Interpreter), then reload the window.

## Dev Tunnel / Codespaces / Remote Port Forwarding Troubleshooting (502)

If you see HTTP ERROR 502 on the forwarded dev tunnel URL (for example `https://<random>-8501.asse.devtunnels.ms`) follow these steps:

1. Check server is running locally and accessible on 8501:

```powershell
# check streamlit is running and that the port is listening
netstat -ano | findstr :8501
# or try requesting locally
curl http://127.0.0.1:8501
```

2. If the server is not running, start it with the correct port (8501 by default) and bind to 0.0.0.0 as shown earlier. If you prefer a different port, set the dev tunnel mapping to the same port.

3. In VS Code/Codespaces dev tunnel or Ports view:
   - Confirm port 8501 is forwarded by the remote environment.
   - Set port 8501 visibility to `Public` and click `Open in Browser`.

4. If the port is forwarded but still 502:
   - Restart the dev tunnel (stop and start it again) or rebuild and restart the Codespace; sometimes stale proxies cause 502 until reconnected.
   - If there's a load balancer or proxy requiring headers, ensure it doesn't strip required headers.

5. On a local system, if you must run the app on port 8080 (for existing dev tunnel settings), start it on 8080 and re-test:

```powershell
& "C:/ProgramData/Anaconda3/python.exe" -m streamlit run aap.py --server.port 8080 --server.address 0.0.0.0
```

## Deployment options

You can deploy this Streamlit application with several providers; here are quick options:

- Streamlit Community Cloud (fast & easy): Connect GitHub and choose `aap.py` as entry; it picks up `requirements.txt` automatically.
- Render: Connect repo to Render, use `render.yaml` or configure build/start commands, setting `--server.port $PORT`.
- Container hosts: The included `Dockerfile` provides a runnable image for Cloud Run, Render Docker, etc.

## Dev helpers in repo
- `start_streamlit.ps1` — Simple PowerShell start script that accepts a port arg for dev use.
- `tests/ui_smoke_playwright.py` — Playwright-based e2e test used by CI to verify UI form and submission.
- `.github/workflows/ci-ui-smoke.yml` — CI that starts Streamlit and runs smoke tests with Playwright.

## Notes
- On Windows prefer the Anaconda/3.11 interpreter for prebuilt binary packages to avoid long compile steps.
- If you encounter issues while deploying to Streamlit Cloud or Render, collect server logs and share them and I can help debug.

