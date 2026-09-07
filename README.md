# Carry

A lightweight, self-hosted project and task management app for individuals and small teams — built with server-rendered Django, HTMX, and Alpine.js.

Carry covers the essentials: projects, tasks, subtasks, comments, labels, and team membership with roles — without the overhead of a SPA or a separate API layer.

## Features

- **Projects** — create projects, track status (Active / Archived / Completed), and manage a global pool of reusable labels
- **Team membership** — invite members with roles (Owner / Admin / Member); owner-only controls for editing and managing membership
- **Tasks** — status and priority tracking, optional assignee and due date, project-scoped label pool
- **Subtasks** — lightweight checklist items with instant toggle (no page reload, via HTMX)
- **Comments** — threaded discussion per task
- **No build step** — HTMX and Alpine.js are loaded as static vendor files; no npm, no bundler, no SPA framework

## Tech Stack

| Layer      | Choice                                |
|------------|---------------------------------------|
| Backend    | Django (server-rendered, no DRF)      |
| Frontend   | HTMX + Alpine.js + Tailwind CSS (CDN) |
| Database   | Sqlite3                               |
| Auth       | Custom `User` model (`accounts` app)  |

## Project Structure

```
pool/
├── apps/
│   ├── accounts/      # Custom User model, auth views
│   ├── core/          # Shared abstract models (TimeStampedModel)
│   ├── projects/      # Projects, membership, project labels
│   ├── tasks/         # Tasks, subtasks, comments, task labels
│   └── home/          # Landing page
├── pool/              # Django settings, root urls.py
├── static/
│   └── vendor/        # htmx.min.js, cdn.min.js (Alpine)
├── templates/         # Global templates (base.html)
├── requirements.txt
└── manage.py
```

Each app follows the same internal layout: `models.py` → `forms.py` → `views.py` → `urls.py` → `admin.py`, with templates under `apps/<app>/templates/<app>/`.

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL running locally (or update `DATABASES` in `pool/settings.py` to point at your instance)

### Setup

```bash
# Clone and enter the project
git clone <your-repo-url>
cd pool

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Run the dev server
python manage.py runserver
```

Visit `http://localhost:8000/` — you'll be redirected to `/home/`. Sign up for an account or log in via `/accounts/login/`, or manage data directly via `/admin/`.

### Creating test data

The Django admin has inline editing set up for quick manual test-data creation:

- **Projects** → add members directly on the project's edit page (inline)
- **Tasks** → add subtasks and comments directly on the task's edit page (inline)

## Key Design Decisions

- **Owner-only permissions (for now)** — only a project's owner can edit the project, manage members, or delete tasks. Any member can view and create. Role-based permissions (e.g. allowing `Admin` members broader access) are a planned enhancement.
- **Global label pools** — `ProjectLabel` and `TaskLabel` are independent, project-agnostic pools rather than project-scoped, keeping label management simple.
- **Nullable task assignee** — tasks can be unassigned; deleting a user unassigns their tasks (`SET_NULL`) rather than deleting the tasks.
- **Subtask toggling bypasses the form layer** — completion checkboxes hit a dedicated lightweight endpoint (`subtask_toggle`) instead of a full `ModelForm` round-trip, since a checkbox flip isn't really a form submission.

## Roadmap

- [ ] Role-based permissions beyond owner-only (Admin role management)
- [ ] Project ownership transfer flow
- [ ] Email notifications for assignments and mentions
- [ ] Production-ready static asset pipeline (currently CDN/vendor-file based)

## License

Add your license here (e.g. MIT).