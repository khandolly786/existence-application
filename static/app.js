const form = document.querySelector("#todo-form");
const input = document.querySelector("#todo-input");
const submitButton = form.querySelector("button");
const list = document.querySelector("#todo-list");
const count = document.querySelector("#todo-count");
const emptyState = document.querySelector("#empty-state");
const statusMessage = document.querySelector("#status-message");

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    let message = "Something went wrong. Please try again.";
    try {
      const body = await response.json();
      message = body.detail || message;
    } catch {
      // Keep the generic message when the server does not return JSON.
    }
    throw new Error(message);
  }

  return response.status === 204 ? null : response.json();
}

function showError(error) {
  statusMessage.textContent = error.message;
}

function renderTodos(todos) {
  list.replaceChildren();
  const remaining = todos.filter((todo) => !todo.completed).length;
  count.textContent = `${remaining} ${remaining === 1 ? "task" : "tasks"} left`;
  emptyState.hidden = todos.length > 0;

  for (const todo of todos) {
    const item = document.createElement("li");
    item.className = `todo-row${todo.completed ? " is-complete" : ""}`;

    const toggle = document.createElement("button");
    toggle.className = "todo-toggle";
    toggle.type = "button";
    toggle.setAttribute("aria-label", todo.completed ? "Mark as not done" : "Mark as done");
    toggle.setAttribute("aria-pressed", String(todo.completed));
    toggle.textContent = todo.completed ? "✓" : "";
    toggle.addEventListener("click", () => updateTodo(todo.id, !todo.completed));

    const title = document.createElement("span");
    title.className = "todo-title";
    title.textContent = todo.title;

    const remove = document.createElement("button");
    remove.className = "todo-delete";
    remove.type = "button";
    remove.setAttribute("aria-label", `Delete ${todo.title}`);
    remove.textContent = "×";
    remove.addEventListener("click", () => deleteTodo(todo.id));

    item.append(toggle, title, remove);
    list.append(item);
  }
}

async function loadTodos() {
  try {
    renderTodos(await request("/api/todos"));
    statusMessage.textContent = "";
  } catch (error) {
    showError(error);
    count.textContent = "Unavailable";
  }
}

async function updateTodo(id, completed) {
  try {
    await request(`/api/todos/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ completed }),
    });
    await loadTodos();
  } catch (error) {
    showError(error);
  }
}

async function deleteTodo(id) {
  try {
    await request(`/api/todos/${id}`, { method: "DELETE" });
    await loadTodos();
  } catch (error) {
    showError(error);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const title = input.value.trim();
  if (!title) {
    showError(new Error("Add a task before submitting."));
    input.focus();
    return;
  }

  submitButton.disabled = true;
  statusMessage.textContent = "";
  try {
    await request("/api/todos", {
      method: "POST",
      body: JSON.stringify({ title }),
    });
    input.value = "";
    await loadTodos();
  } catch (error) {
    showError(error);
  } finally {
    submitButton.disabled = false;
    input.focus();
  }
});

loadTodos();
