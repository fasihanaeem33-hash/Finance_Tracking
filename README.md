<<<<<<< HEAD
# Personal Finance Tracker — Setup & Run

This repository contains a Streamlit-based personal finance tracker (`aap.py`). To run it and resolve editor diagnostics, follow the steps below.

1. Install the dependencies listed in `requirements.txt` with the Python you use for this workspace (the same interpreter selected into VS Code). Example (Windows PowerShell):

```powershell
# Using Python 3.11+ (recommended for Windows because many packages provide prebuilt wheels):
"C:/Program Files/Python311/python.exe" -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install --upgrade pip; pip install -r requirements.txt

# OR if you already use system Python (replace with your installed path):
"C:/Program Files/Python313/python3.13t.exe" -m pip install -r requirements.txt
```
- If you are using Python 3.13 and `pip install` fails while building packages like `pandas`, consider installing Python 3.11 or use a conda/mamba environment which provides binary packages for Windows. Example:

```powershell
# Using conda/mamba:
mamba create -n finance-tracker python=3.11 -y
mamba activate finance-tracker
python -m pip install -r requirements.txt
```


2. In VS Code, ensure the Python Interpreter is set to the same Python that has the packages installed:
   - Open the Command Palette (Ctrl+Shift+P)
   - Select `Python: Select Interpreter` and choose your interpreter (for Windows, Anaconda is recommended if you have it installed):
     - Example: `C:/ProgramData/Anaconda3/python.exe` or `C:/Users/admin/Desktop/Finance_Tracking/.venv/Scripts/python.exe`

3. Run the Streamlit app:

```powershell
# Example (Anaconda):
"C:/ProgramData/Anaconda3/python.exe" -m streamlit run aap.py

# Example (workspace venv):
"C:/Users/admin/Desktop/Finance_Tracking/.venv/Scripts/python.exe" -m streamlit run aap.py
```

4. If you still see `import ... could not be resolved` in the editor after installing the packages and selecting the right interpreter, try this:
   - Reload VS Code window (Ctrl+Shift+P -> `Developer: Reload Window`)
   - Restart Pylance server or re-open project

Tips:
- Consider creating a virtual environment for the project and installing packages there for reproducibility:
  ```powershell
  "C:/Program Files/Python313/python3.13t.exe" -m venv .venv; .\.venv\scripts\Activate.ps1; python -m pip install -r requirements.txt
  ```

Deployment options
------------------

You can deploy this Streamlit application using several providers; here are a few simple ways:

1) Streamlit Community Cloud (recommended and easiest)
   - Sign in to Streamlit Cloud (https://streamlit.io/cloud) with your GitHub account.
   - Click New app -> Choose repo -> Provide `aap.py` as the main file and `requirements.txt` for dependencies.
   - Streamlit will build the app and give you a public URL.

2) Render
   - Create a Render account (https://render.com) and connect your GitHub.
   - Create a new web service pointing at this repo. The `render.yaml` file is included to help configure deployment automatically.
   - Configure env var `PORT` (Render sets this automatically) and start command: `streamlit run aap.py --server.port $PORT --server.address 0.0.0.0`.

3) GitHub Container Registry + Any container host (Docker, Kubernetes, Render/Cloud Run)
   - GitHub Action `build-and-push-image.yml` builds and publishes a Docker image to GitHub Container Registry (`ghcr.io`), tag: `finance-tracker:latest`.
   - Use that image with any container hosting provider.

4) Heroku (deprecated free tier — proceed with caution)
   - Add a Procfile (included) and `requirements.txt`.
   - Push to Heroku or connect the repo with Heroku Dashboard and deploy.

Notes:
 - On Windows, prefer using Python 3.11 or a conda-based environment to avoid heavy builds when installing `pandas`. Docker or Render's build environment often uses pre-built wheels.
 - If you choose to use the workspace `.venv`, be sure to set VS Code to use `.venv/Scripts/python.exe` and re-run the app.

=======
**Link for Streamlit**
https://fictional-fortnight-x5g9pr4wqgqx364x9-8501.app.github.dev/

https://fictional-fortnight-x5g9pr4wqgqx364x9-8501.app.github.dev/

**Overview**
While building the Streamlit personal finance tracking app, I learned how to manage and organize financial data using Python,
Streamlit components, and simple data structures like lists and dictionaries. I understood how to create an interactive interface 
where users can input income, expenses, and investments, and instantly see summaries or visualizations. I also learned how powerful
Streamlit is for quickly turning Python scripts into user-friendly applications without complex front-end coding. Overall, this project
helped me strengthen my skills in data handling, UI design, and real-time financial tracking.

**Dashboard Screenshot** 
<img width="1366" height="768" alt="Dashboard PFinance 2025-11-27 14 36 44" src="https://github.com/user-attachments/assets/8b9b0a2c-54ff-49bf-b738-cdff72db6f0a" />
>>>>>>> 452417eded1b1db646dd66770d6b60cca67a25dc
