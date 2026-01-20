# Task 008: Enhanced Personal Website

I have enhanced the personal website with a light/dark mode toggle.

## New Features
- **Theme Switcher**: a floating button to toggle between light and dark modes.
- **Persistence**: Remembers your theme preference using local storage.
- **System Preference**: Defaults to your system's color scheme if no preference is saved.

## Features
- **Modern Design**: Clean interface with a dark/light mode adaptable theme.
- **Responsive**: Works on desktop and mobile.
- **Dynamic Links**: Easily configurable links in `app.py`.
- **Custom Logo**: Includes a generated abstract logo.

## How to Run

1.  Navigate to the project directory:
    ```bash
    cd 008_personal-website-enhanced
    ```
2.  Run the Flask application:
    ```bash
    ../venv/bin/python3 app.py
    ```
3.  Open your browser and go to `http://127.0.0.1:5000`.

## Verification Scenarios

-   [x] **Server Start**: Confirmed the Flask server starts without errors.
-   [x] **Theme Toggle**: Clicking the button switches themes instantly.
-   [x] **Icons**: The sun/moon icons switch correctly.
-   [x] **Persistence**: Reloading the page retains the selected theme.

## Troubleshooting

-   **X (Twitter) Feed Not Loading?**: Ensure you are not using an ad-blocker or strict tracking protection (like Privacy Badger), as these often block the X widget script. Also, X may rate-limit anonymous views.

