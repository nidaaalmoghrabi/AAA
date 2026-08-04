# Task Tracker API

Task Tracker API is a small REST API learning project built with Python and FastAPI. It provides task CRUD endpoints, a simple browser-based task board, due dates with overdue filtering, and an in-memory activity log without authentication, database storage, or cloud deployment.

## Features

- Create, list, read, update, and delete tasks.
- Track task title, description, status, priority, assignee, and optional due date.
- Filter tasks by status, priority, or overdue state.
- Show due and overdue indicators on frontend task cards.
- Record simple activity events for task create, update, status change, and delete.
- View all activity or activity for a single task.

## Requirements

- Python 3.10 or newer
- `pip`

## Project Structure

```text
task-tracker-api/
|
|-- app/
|   |-- __init__.py
|   |-- business_rules.py
|   |-- main.py
|   |-- models.py
|   |-- repository.py
|   |-- routes.py
|   `-- storage.py
|
|-- frontend/
|   `-- index.html
|
|-- tests/
|   |-- __init__.py
|   |-- conftest.py
|   |-- test_health.py
|   `-- test_tasks.py
|
|-- .dockerignore
|-- .env.example
|-- Dockerfile
|-- README.md
`-- requirements.txt
```

Module responsibilities:

- `app/main.py`: FastAPI app instance, CORS middleware, demo data seeding, and the task/activity route handlers.
- `app/models.py`: Pydantic request/response schemas and field validation (e.g. title trimming).
- `app/business_rules.py`: Status-transition validation (`validate_status_transition`).
- `app/storage.py`: In-memory task and activity store.
- `app/repository.py`: Generic in-memory repository base class.
- `app/routes.py`: The `/health` route.

Every public function and route handler in `app/` has a Google-style docstring (summary, `Args`, `Returns`, `Raises`, and an `Example` for route handlers). Keep new public functions documented the same way; private helpers (leading underscore) are exempt.

## Create a Virtual Environment

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

After activation, the terminal normally displays the virtual environment name before the command prompt.

## Install Dependencies

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the project dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configure Environment Variables

Copy the example environment file.

### Linux/macOS

```bash
cp .env.example .env
```

### Windows PowerShell

```powershell
Copy-Item ".env.example" ".env"
```

The default configuration is:

```dotenv
PORT=8000
APP_ENV=development
```

## Start the Development Server

Run the following command from the project root:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The API and task board frontend will be available at:

```text
http://127.0.0.1:8000
```

The automatic Swagger UI documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema will be available at:

```text
http://127.0.0.1:8000/openapi.json
```

## Task API

Create a task:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Write README\",\"assignee\":\"Alicia\",\"due_date\":\"2026-08-03\"}"
```

List tasks:

```bash
curl http://127.0.0.1:8000/tasks
```

Filter overdue tasks:

```bash
curl "http://127.0.0.1:8000/tasks?overdue=true"
```

Update a task:

```bash
curl -X PATCH http://127.0.0.1:8000/tasks/TASK_ID \
  -H "Content-Type: application/json" \
  -d "{\"assignee\":\"Marcus\"}"
```

Delete a task:

```bash
curl -X DELETE http://127.0.0.1:8000/tasks/TASK_ID
```

## Activity API

The activity log records task create, update, status-change, and delete events.

View all activity:

```bash
curl http://127.0.0.1:8000/activity
```

View activity for one task:

```bash
curl http://127.0.0.1:8000/tasks/TASK_ID/activity
```

Activity update events only include fields that actually changed. For example, changing only the assignee records:

```text
updated assignee
```

Changing status records the previous and next status:

```text
changed status from ToDo to InProgress
```

Deleting a task records:

```text
deleted task
```

## Test the Health Endpoint with curl

Keep the Uvicorn server running and open another terminal.

Run:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "timestamp": "2026-07-20T19:30:15.245721Z"
}
```

The exact timestamp will be different for every request.

## Run the Automated Tests

From the project root, run:

```bash
python -m pytest
```

For more detailed output, run:

```bash
python -m pytest -v
```

## Run with Docker

Build the image from the project root:

```bash
docker build -t task-tracker-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 task-tracker-api
```

The image is a multi-stage build (builder + slim runtime), runs as a non-root `app` user, and exposes a container `HEALTHCHECK` against `GET /health`. The API and frontend are then available at `http://127.0.0.1:8000`, same as the local dev server.

## Continuous Integration

Pushes and pull requests run the `c1` GitHub Actions workflow, which installs dependencies and runs `python -m pytest -v --tb=short` against Python 3.11. The workflow file lives at the repository root (`.github/workflows/c1.yml`, one level above `task-tracker-api/`) rather than inside this project directory, because GitHub only triggers workflows found under `.github/workflows` at the repo root, and sets `task-tracker-api` as its working directory.

## Business Rules

- Valid task status transitions: `ToDo -> InProgress`, `InProgress -> Done`, `Done -> InProgress`.
- Invalid transitions (e.g. `ToDo -> Done`, `Done -> ToDo`, or setting the same status again) return `422`.
- `title` is required, trimmed, and must not be blank or exceed 200 characters.

## Stop the Server

Press:

```text
Ctrl+C
```

in the terminal where Uvicorn is running.
