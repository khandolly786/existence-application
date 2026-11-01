# Low-Level Design

## Backend

The backend is implemented in `main.py` with FastAPI and Python's built-in `sqlite3` module.

### Database

The `todos` table is initialized when the application module loads:

| Column | Type | Details |
|---|---|---|
| `id` | INTEGER | Primary key, auto-incrementing |
| `title` | TEXT | Required todo title |
| `completed` | INTEGER | Required; defaults to `0` |
| `created_at` | TEXT | Required; defaults to SQLite `CURRENT_TIMESTAMP` |

Database connections use `sqlite3.Row`, allowing todo records to be serialized into JSON objects with `id`, `title`, `completed` (as a boolean), and `created_at`.

### API

| Method | Path | Behavior |
|---|---|---|
| `GET` | `/api/todos` | Returns todos ordered by descending ID. |
| `POST` | `/api/todos` | Creates a todo. Trims the title; rejects an empty title or one longer than 200 characters. Returns the created todo with status `201`. |
| `PATCH` | `/api/todos/{todo_id}` | Updates the `completed` state. Returns `404` if the todo does not exist. |
| `DELETE` | `/api/todos/{todo_id}` | Deletes a todo. Returns `404` if the todo does not exist; otherwise returns status `204`. |

The root route (`GET /`) serves `static/index.html`. The `/static` mount serves the frontend assets.

## Frontend

- `static/index.html` contains the add form, task list, remaining-task count, status message, and empty-list state.
- `static/style.css` defines the layout, colors, typography, task states, and a narrow-screen layout.
- `static/app.js` loads todos on startup, renders the list, submits new tasks, toggles completion, deletes tasks, and displays request errors.
- Todo text is inserted using `textContent`. The form and completion controls also include accessible labels and status attributes.
- The JavaScript uses `GET /api/todos`, `POST /api/todos`, `PATCH /api/todos/{todo_id}`, and `DELETE /api/todos/{todo_id}`.

## Dependencies

- FastAPI (`fastapi`)
- Uvicorn (`uvicorn[standard]`)
- SQLite via Python's standard library
