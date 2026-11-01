# High-Level Design

## Application Overview

Little List is a single-page todo application. Its browser-based interface is built with HTML, CSS, and JavaScript. A FastAPI server delivers the interface, exposes a JSON API, and stores todo items in a local SQLite database.

## Architecture

```text
Browser
  ├── GET /              → FastAPI serves static/index.html
  ├── /static/style.css  → FastAPI serves the stylesheet
  ├── /static/app.js     → FastAPI serves the client application
  └── /api/todos         → FastAPI todo API
                            └── SQLite (todos.db)
```

### Components

- **Frontend:** `static/index.html`, `static/style.css`, and `static/app.js` provide the todo interface and call the API using `fetch`.
- **Backend:** `main.py` defines the FastAPI application, serves the page and static assets, validates todo input, and handles todo operations.
- **Database:** SQLite stores todo titles, completion state, and creation timestamps in `todos.db`, created next to `main.py`.

## Data Flow

1. The browser requests `/`; the server responds with the HTML page.
2. The page loads its CSS and JavaScript from `/static`.
3. The JavaScript requests `/api/todos` and renders the returned todo items.
4. Create, completion-toggle, and delete actions send JSON API requests to the server.
5. The server reads or updates SQLite and returns the result; the browser refreshes the displayed list.
