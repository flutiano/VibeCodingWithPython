/*
Task 009: deploy the personal website developed in Task 008 to Cloud service provider so that it is accessible publicly. For the cloud provider, I am thinking of PythonAnywhere by Anaconda, who provides a free tier that I can use.
*/

# Task 009: Deploy Personal Website to PythonAnywhere

This task provides the necessary scripts and guidance to deploy the personal website created in Task 008 to PythonAnywhere.

## Contents
- `prepare_files.sh`: Script to bundle website files into a ZIP archive.
- `wsgi_config_template.py`: Template for PythonAnywhere's WSGI configuration.
- `deployment_guide.md`: Step-by-step instructions for the deployment process.

## Walkthrough: Deployment Process

I have prepared all the necessary materials and successfully executed the deployment to PythonAnywhere.

### Changes Made
- Created `prepare_files.sh`: Bundles the Flask application into `website.zip`.
- Created `wsgi_config_template.py`: Template for the server's WSGI configuration.
- Created `deployment_guide.md`: Detailed manual steps for PythonAnywhere.

### Testing and Validation
The deployment was verified by navigating to the live URL: [https://flutiano.pythonanywhere.com/](https://flutiano.pythonanywhere.com/)

**Homepage Verification:**
![Homepage Verification](/Users/jeffzo/.gemini/antigravity/brain/435e1eb6-1681-408f-8de8-a16efd2fe71e/homepage_verification_1768996901456.png)

### Deployment Process Recordings
Automated deployment steps captured via browser subagent:

````carousel
![Files Upload Attempt](/Users/jeffzo/.gemini/antigravity/brain/435e1eb6-1681-408f-8de8-a16efd2fe71e/pythonanywhere_files_upload_1768995779263.webp)
<!-- slide -->
![Console Setup](/Users/jeffzo/.gemini/antigravity/brain/435e1eb6-1681-408f-8de8-a16efd2fe71e/pythonanywhere_console_setup_1768996248727.webp)
<!-- slide -->
![Web App Config](/Users/jeffzo/.gemini/antigravity/brain/435e1eb6-1681-408f-8de8-a16efd2fe71e/pythonanywhere_web_app_config_1768996443792.webp)
<!-- slide -->
![Live Verification](/Users/jeffzo/.gemini/antigravity/brain/435e1eb6-1681-408f-8de8-a16efd2fe71e/pythonanywhere_live_verification_1768996881996.webp)
````

## Example Output (Bundling Script)
```bash
$ ./prepare_files.sh
Bundling files from ../008_personal-website-enhanced...
  adding: requirements.txt (stored 0%)
  adding: static/ (stored 0%)
  adding: static/logo.png (deflated 3%)
  adding: static/style.css (deflated 72%)
  adding: app.py (deflated 42%)
  adding: templates/ (stored 0%)
  adding: templates/index.html (deflated 64%)
Success! Archive website.zip has been created.
You can now upload this file to PythonAnywhere.
```

## Dependencies
The website itself requires `Flask`.
```text
Flask==3.0.0
```

## Final Status
Website is **LIVE** at [https://flutiano.pythonanywhere.com/](https://flutiano.pythonanywhere.com/)
