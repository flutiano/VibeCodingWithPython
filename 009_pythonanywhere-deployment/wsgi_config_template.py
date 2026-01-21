# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It clarifies which directory your code is in, and where your flask
# app object is located.

import sys

# add your project directory to the sys.path
path = '/home/<your-username>/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application  # noqa
