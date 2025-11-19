Here is a clean, structured, professional **README for your `templates/` folder**, matching the tone and format of your other project documentation.

No horizontal rules.
Concise, intuitive, and informative.

---

# 📁 `templates/` Folder — HTML Templates Overview

This folder contains all **HTML templates** used by the AI Medical Chatbot Flask application.
Flask renders these templates through `render_template()`, combining server-side data with Jinja2 logic to produce the final user-facing web pages.

## Contents

### 🖥️ `index.html`

The main user interface for the chatbot.
It displays:

* The app header (title, subtitle, online indicator)
* Chat history pulled from the Flask session
* User and assistant messages rendered with Jinja filters
* Error notifications passed from the backend
* Input form for medical questions
* Button for clearing the chat session
* Footer disclaimer with medical safety notice

The template uses:

* Jinja2 loops and conditionals to show messages
* The custom `nl2br` filter for newline formatting
* Accessible markup with labels and semantic structure
* Auto-scroll JavaScript to keep view on the latest message

## Purpose

The `templates/` directory defines the **structure and dynamic rendering** of the chatbot’s front-end.
It determines what the user sees and how server-provided data appears in the browser.

Flask automatically searches this folder for templates, making it the central location for all HTML views in the project.

If additional pages (e.g. an About page, logs viewer, admin dashboard) are added in the future, they should also be placed here.
