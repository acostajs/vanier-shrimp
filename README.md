# Shrimp

Vanier College Learning Integration Assessment (LIA) project.

**Shrimp** is a social news website built with **Flask**, inspired by platforms like Hacker News and Lobsters. The application allows users to share news links, discuss them through comments, and interact using authenticated user accounts.

The project focuses on backend web development fundamentals, including RESTful routing, database modeling, authentication, form validation, and server-rendered templates using Jinja.

---

## Features

- Submit news stories with a title, link, and optional description
- View all stories sorted from most recent to oldest
- Comment on stories with threaded discussion per post
- User account system with registration, login, and logout
- Stories and comments are linked to authenticated users
- Input validation and error handling for all forms
- Flash messages for user actions (registration, login, logout, comments)
- Human-readable timestamps (e.g. “2 hours ago”)

---

## Tech Stack

- **Backend:** Flask  
- **Templating:** Jinja  
- **Database:** SQLite  
- **ORM:** SQLAlchemy  
- **Authentication:** Flask session-based auth  
- **Environment & Packaging:** uv  

---

## Project Structure

```text
shrimp/
├── shrimp/
│   ├── accounts/        # User registration and authentication
│   ├── stories/         # Stories and comments logic
│   ├── templates/       # Jinja templates
│   ├── static/          # Static assets
│   ├── models.py        # Database models
│   └── __init__.py      # App factory
├── instance/
│   └── site.db          # SQLite database (gitignored)
└── pyproject.toml
````

---

## Setup & Run

### 1. Clone the repository

```sh
git clone <repo>
cd shrimp
```

### 2. Initialize the database

```sh
uv run flask --app shrimp init
```

### 3. Run the development server

```sh
uv run flask --app shrimp run --debug
```

The application will be available at:

```
http://127.0.0.1:5000
```

---

## Usage Overview

* Create an account to submit stories and post comments
* Browse the home page to see recently submitted stories
* Click a story to view its description and comments
* Leave comments while logged in
* Log out to return to read-only access

---

## Notes

* This is a server-rendered application with no front-end framework
* The focus is on backend logic, data relationships, and validation
* Designed for clarity, correctness, and academic evaluation

---

## Academic Disclaimer

This project was developed for academic purposes as part of a Vanier College Learning Integration Assessment. It demonstrates understanding of Flask, database-backed applications, and user authentication workflows.
