# 📁 `static/` Folder — Front-End Assets Overview

This folder contains all **front-end static assets** used by the AI Medical Chatbot Flask application.
Files in this directory are served directly by Flask via `url_for('static', ...)` and are responsible for the **visual presentation**, **layout**, and **client-side behaviour** of the web interface.

## Contents

### 🎨 `style.css`

Defines the full UI styling for the chatbot, including:

* Page layout and card structure
* Header, subtitles, and online status indicator
* Scrollable chat container
* User and assistant message formatting
* Input panel, text areas, and buttons
* Error banners and empty-state design
* Footer disclaimer styling
* Custom scrollbar appearance
* Accessibility helpers such as `.sr-only`

It is fully documented with intuitive inline comments to support easy modification or extension.

### 🖼️ Images (if added)

Any icons, logos, or visual assets placed here will be publicly accessible and can be referenced directly in templates using the Flask static path helper.

## Purpose

The `static/` directory provides all client-side styling and ensures the chatbot interface remains:

* Clear and accessible
* Mobile-friendly
* Visually consistent
* Easy to maintain or customise

If you need an additional JS file, custom fonts, or images, they can be safely added here and will automatically become available to the Flask app.
