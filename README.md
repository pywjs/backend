# pywjs FastAPI backend
![example workflow](https://github.com/pywjs/backend/actions/workflows/test.yaml/badge.svg)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/pywjs/backend)
[![](https://img.shields.io/github/license/pywjs/pywjs.svg)](https://github.com/pywjs/pywjs/blob/main/LICENSE)
![t](https://img.shields.io/badge/status-maintained-blue.svg)

The FastAPI Backend for the pywjs core.

Main features:
- FastAPI
- uvicorn
- pytest
- ruff
- SQLAlchemy
- Alembic
- asyncpg
- SQLModel
- asyncio

Main apps:
- core: settings, DB operations, and common utilities, models, and abstract classes
- auth: Authentication and authorization (User model agnostic)
- users: User management (CRUD operations)
- CMS: Content management system (CRUD operations)
  - posts: Post management (CRUD operations)
  - pages: Page management (CRUD operations)
  - navigation: Navigation management (CRUD operations)
- upload: File upload and management (Storage backend agnostic, supports local and S3 storage)
- search: Search engine (Elasticsearch or PostgreSQL)
- notifications: Notification system (Email, SMS, WebSocket)
