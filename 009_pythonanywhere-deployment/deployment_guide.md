# PythonAnywhere Deployment Guide

Follow these steps to deploy your personal website to PythonAnywhere.

## 1. Prepare Local Files
Run the preparation script in your terminal to bundle your files into `website.zip`:
```bash
cd 009_pythonanywhere-deployment
chmod +x prepare_files.sh
./prepare_files.sh
```

## 2. Upload to PythonAnywhere
1. Log in to your [PythonAnywhere account](https://www.pythonanywhere.com/).
2. Go to the **Files** tab.
3. In the "Upload a file" section, upload the `website.zip` you just created.
4. Open a **Bash Console** from the dashboard.
5. In the console, create a directory for your site and unzip the files:
   ```bash
   mkdir -p mysite
   unzip website.zip -d mysite
   rm website.zip
   ```

## 3. Set Up Virtual Environment
In the same Bash console, run:
```bash
mkvirtualenv --python=/usr/bin/python3.10 mysite-venv
pip install Flask
# Note: If you have other dependencies in requirements.txt, run:
# pip install -r mysite/requirements.txt
```

## 4. Configure Web App
1. Go to the **Web** tab on PythonAnywhere.
2. Click **Add a new web app**.
3. Select **Manual configuration** (do NOT select "Flask").
4. Choose **Python 3.10**.
5. After creation, find the **Virtualenv** section and enter:
   `/home/<your-username>/.virtualenvs/mysite-venv`
6. Locate the **WSGI configuration file** link (usually `/var/www/<your-username>_pythonanywhere_com_wsgi.py`). Click it to edit.
7. Replace the content with the provided template (updating `<your-username>`):
   ```python
   import sys
   path = '/home/<your-username>/mysite'
   if path not in sys.path:
       sys.path.insert(0, path)

   from app import app as application
   ```
8. Save the file.

## 5. Reload and Verify
1. Go back to the **Web** tab.
2. Click the green **Reload** button.
3. Visit `http://<your-username>.pythonanywhere.com` to see your live site!

## Troubleshooting
- **Error Logs**: If the site shows an error, check the "Error log" link on the Web tab.
- **Static Files**: If CSS/images are missing, go to the Web tab -> **Static files** section and add:
    - URL: `/static/`
    - Directory: `/home/<your-username>/mysite/static`
