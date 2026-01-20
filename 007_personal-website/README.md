# Task 007: Personal Website Walkthrough

I have built a modern, minimalist personal website using Flask.

## Features
- **Modern Design**: Clean interface with a dark/light mode adaptable theme.
- **Responsive**: Works on desktop and mobile.
- **Dynamic Links**: Easily configurable links in `app.py`.
- **Custom Logo**: Includes a generated abstract logo.

## How to Run

1.  Navigate to the project directory:
    ```bash
    cd 007_personal-website
    ```
2.  Run the Flask application:
    ```bash
    ../venv/bin/python3 app.py
    ```
3.  Open your browser and go to `http://127.0.0.1:5000`.

## Customization

-   **Links**: Edit the `links` list in `app.py` to add or remove social media links.
-   **Styles**: Modify `static/style.css` to change colors or fonts.
-   **Logo**: Replace `static/logo.png` with your own image if desired.

## Verification Scenarios

-   [x] **Server Start**: Confirmed the Flask server starts without errors.
-   [x] **Home Page**: Verified the home page serves 200 OK.
-   [ ] **Visual Check**: User to verify the aesthetics and interactions in the browser.
