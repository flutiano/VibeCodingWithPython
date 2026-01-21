# Deployment of Personal Website to PythonAnywhere

This task involves deploying the Flask-based personal website (from Task 008) to PythonAnywhere to make it publicly accessible.

## Proposed Changes

### [New Deployment Directory]
#### [NEW] [deployment_guide.md](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/009_pythonanywhere-deployment/deployment_guide.md)
A comprehensive step-by-step guide for the user to follow in the PythonAnywhere interface and console.

#### [NEW] [prepare_files.sh](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/009_pythonanywhere-deployment/prepare_files.sh)
A script to bundle the website files into a ZIP archive for easy upload to PythonAnywhere.

#### [NEW] [wsgi_config_template.py](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/009_pythonanywhere-deployment/wsgi_config_template.py)
A template for the WSGI configuration file required by PythonAnywhere.

#### [NEW] [README.md](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/009_pythonanywhere-deployment/README.md)
Task documentation as per the project rules.

#### [NEW] [Plan.md](file:///Users/jeffzo/projects/practice/AIcoding/VibeCodingWithPython/009_pythonanywhere-deployment/Plan.md)
Saved implementation plan as per the project rules.

## Verification Plan

### Manual Verification
1. **Bundle Verification**: Ensure the `prepare_files.sh` script correctly creates a `website.zip` containing all necessary files (`app.py`, `static/`, `templates/`, `requirements.txt`).
2. **Deployment Walkthrough**: The user will follow the `deployment_guide.md` to:
    - Upload the ZIP to PythonAnywhere.
    - Set up a virtual environment.
    - Configure the WSGI file.
    - Reload and verify the public URL.
3. **Public Access**: Verify that the website is live and functional (theme switcher, navigation) at `http://<yourusername>.pythonanywhere.com`.
