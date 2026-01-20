# Task: Create a Python program for a personal website with a logo in the center, and links to my YouTube, Twitter, and Gumroad page.
# The design should be modern and minimalist.
# Improved: Add a button to toggle between light and dark themes.

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    links = [
        {"name": "YouTube", "url": "https://www.youtube.com/@jeffreyzhao6351", "icon": "youtube"},
        {"name": "X", "url": "https://x.com/flutiano", "icon": "x-logo"},
        {"name": "Gumroad", "url": "https://gumroad.com", "icon": "shopping-bag"},
    ]
    
    return render_template('index.html', links=links)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Example Output:
#  * Serving Flask app 'app'
#  * Debug mode: on
# WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
#  * Running on http://127.0.0.1:5000
# Press CTRL+C to quit
#  * Restarting with stat
#  * Debugger is active!
#  * Debugger PIN: 751-610-132
