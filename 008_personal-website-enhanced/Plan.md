# Task 008: Theme Switcher for Personal Website

The goal is to enhance the existing personal website from Task 007 by adding a manual toggle between light and dark themes.

## Proposed Changes

### 1. `008_personal-website-enhanced/app.py`
- Update the top-level comment to reflect the new task prompt.

### 2. `008_personal-website-enhanced/static/style.css`
- Refactor CSS variables to support class-based theming (e.g., `body.light-mode`).
- Add styles for the theme toggle button.

### 3. `008_personal-website-enhanced/templates/index.html`
- Add a theme toggle button (icon based).
- Add JavaScript to:
    - Handle button click.
    - Toggle the `light-mode` class on `body`.
    - Persist user preference in `localStorage`.
    - Initialize based on `localStorage` or system preference.

### 4. `008_personal-website-enhanced/README.md`
- Update documentation to include the new feature.

## Verification Plan

### Manual Verification
- **Toggle Test**: Click the theme button and verify colors change immediately.
- **Persistence Test**: Reload the page to ensure the chosen theme remains (using `localStorage`).
- **Responsive Test**: Ensure the button is accessible on mobile.
