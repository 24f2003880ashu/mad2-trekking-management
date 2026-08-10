# Trekking Management Application V2

Modern Application Development II Project

## Project Description

Trekking Management Application is a web-based application for managing trekking activities, users, staff, bookings and trek information.

The application provides separate functionality for Admin, Staff and Users.

## Technology Stack

- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Vue.js
- Vue Router
- Axios
- Bootstrap
- SQLite
- Redis
- Celery
- MailHog

## Project Structure

```text
mad2-trekking-management/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── config.py
│   ├── tasks.py
│   ├── celery_worker.py
│   ├── celeryconfig.py
│   └── mail_service.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── api.yaml
├── mad2_project_report.pdf
└── README.md