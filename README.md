# Little List

A deliberately small starter todo app: plain HTML, CSS, and JavaScript on the
frontend, FastAPI for the API, and SQLite 3 for storage.

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the server with `uvicorn main:app --reload`.
4. Open <http://127.0.0.1:8000>.

The SQLite database (`todos.db`) is created automatically next to `main.py`.
The API docs are available at <http://127.0.0.1:8000/docs>.

## Included so far

- Add a todo
- Mark a todo done or not done
- Delete a todo
- Keep todos after restarting the server

This is intentionally a first slice, not a finished product: there is no
editing, filtering, sign-in, or polished loading experience yet.
