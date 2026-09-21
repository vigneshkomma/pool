# Pool

A project and task management web app for individuals and small teams. Built with Django and HTMX, fully server-rendered.

## Features

- Projects with owner and member roles
- Tasks with status, priority, assignee, and subtasks
- Comments on tasks
- Global label pools for projects and tasks
- Owner-only editing, deletion, and member management; project viewing is limited to members
- Dashboard of your projects after login
- Inline subtask toggling via HTMX (no page reload)

## Tech Stack

- **Backend:** Django (server-rendered, no DRF)
- **Frontend:** HTMX and Alpine.js (vendored static files), Tailwind CSS via CDN
- **Database:** PostgreSQL

## Project Structure

```
pool/
├── apps/
│   ├── accounts/   # Custom User model (extends AbstractUser)
│   ├── projects/   # Projects, members, project labels
│   ├── tasks/      # Tasks, subtasks, comments, task labels
│   └── home/       # Landing page
├── core/           # Shared code (abstract TimeStampedModel)
├── static/         # Vendored HTMX and Alpine.js
├── templates/
├── manage.py
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL

### Setup

```bash
# Clone the repository and enter it
git clone <your-repo-url> pool
cd pool

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Create a PostgreSQL database and update the `DATABASES` setting in your Django settings to match it.

```bash
# Apply migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser. The admin site is at `/admin/`.

## Key Design Decisions

- **Custom User model** in `accounts`, set up before the first migration.
- **HTMX for interactivity:** the CSRF token is sent globally through `hx-headers` on `<body>`, and subtask toggling is a dedicated endpoint returning an HTML partial.
- **Delete behavior:** `RESTRICT` on owner/creator foreign keys, `SET_NULL` on task assignee, `CASCADE` for tasks, subtasks, and comments.
- **Enums** use Django `TextChoices` (`Status`, `Priority`, `Role`).
- **Assignees** are restricted to members of the task's project.

## Development Notes

- Commit migrations; do not commit generated files (`__pycache__/`, `*.pyc`, `.idea/`, `db.sqlite3`).
- Vendor files live under `static/` and are served through `STATICFILES_DIRS`.
- Dependencies are tracked in a single `requirements.txt` (`pip freeze > requirements.txt`).

## Status

Approaching MVP. Not yet covered: production/deployment settings and automated tests.