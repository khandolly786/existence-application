from pathlib import Path
import sqlite3
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DATABASE_PATH = BASE_DIR / "todos.db"

app = FastAPI(title="Half-Baked Todo")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    completed: bool


def connect_db() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db() -> None:
    with connect_db() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def serialize_todo(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"]),
        "created_at": row["created_at"],
    }


initialize_db()


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/todos")
def list_todos() -> list[dict[str, Any]]:
    with connect_db() as connection:
        rows = connection.execute(
            "SELECT id, title, completed, created_at FROM todos ORDER BY id DESC"
        ).fetchall()
    return [serialize_todo(row) for row in rows]


@app.post("/api/todos", status_code=201)
def create_todo(todo: TodoCreate) -> dict[str, Any]:
    title = todo.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="Todo title cannot be empty.")
    if len(title) > 200:
        raise HTTPException(status_code=422, detail="Todo title must be 200 characters or fewer.")

    with connect_db() as connection:
        cursor = connection.execute("INSERT INTO todos (title) VALUES (?)", (title,))
        row = connection.execute(
            "SELECT id, title, completed, created_at FROM todos WHERE id = ?",
            (cursor.lastrowid,),
        ).fetchone()
    return serialize_todo(row)


@app.patch("/api/todos/{todo_id}")
def update_todo(todo_id: int, update: TodoUpdate) -> dict[str, Any]:
    with connect_db() as connection:
        cursor = connection.execute(
            "UPDATE todos SET completed = ? WHERE id = ?",
            (int(update.completed), todo_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found.")
        row = connection.execute(
            "SELECT id, title, completed, created_at FROM todos WHERE id = ?",
            (todo_id,),
        ).fetchone()
    return serialize_todo(row)


@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    with connect_db() as connection:
        cursor = connection.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Todo not found.")
