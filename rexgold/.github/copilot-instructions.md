## Purpose
Short, actionable guide for AI code assistants to be productive in this repository.

## Big-picture architecture
- Django monolith laid out as multiple Django apps inside the `rexgold/` package (apps like `Account_Module`, `Order_Module`, `Product_Data_Module`, etc.).
- Top-level Django project package is `rexgold` (settings in `rexgold/settings.py`, URLs in `rexgold/urls.py`).
- REST API powered by Django REST Framework; API schemas generated with `drf-spectacular` (endpoints: `/schema`, `/schema/swagger-ui/`, `/schema/redoc/`).
- Auth: custom user model `Account_Module.User` with JWT authentication (`rest_framework_simplejwt`).
- Background & realtime: Celery + Redis configuration present (broker/result Redis at 127.0.0.1:6379), Channels configured to use Redis channel layers.

## How to run (developer workflows)
- Local venv: repository contains a suggested venv `venv-rexgold/`. Typical flow:
  - Activate virtualenv (shell-specific). Install deps with `pip install -r requirements.txt` (file at repo root).
  - Run migrations: `python manage.py migrate`.
  - Run dev server: `python manage.py runserver 0.0.0.0:8000` (Dockerfile and docker-compose also start the dev server).
- Docker: `Dockerfile` uses `python:3.11-slim` and runs `manage.py runserver`. `docker-compose.yml` mounts the repo and exposes 8000.
- Celery: project sets `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` to Redis. To run workers, use the standard Celery invocation for this project: `celery -A rexgold worker -l info` (needs Redis running).
- Tests: use Django test runner: `python manage.py test`. The project uses per-app `tests.py` files.

## Key patterns & conventions (project-specific)
- App naming: modules use PascalCase with `_Module` suffix (e.g., `Order_Module`). Look for `models.py`, `serializers.py`, `views.py`, `urls.py` in each app.
- Serializers <-> models: Many serializers return or expect model instances rather than plain IDs. Example: `Order_Module/views.py` passes `product` and `user` objects to `Order.objects.create(...)` (comments indicate object, not id).
- Views: mix of `viewsets.ModelViewSet` and `APIView` is used. Filters commonly use `django_filters.rest_framework.DjangoFilterBackend` and custom `filters.py` in apps (e.g., `Order_Module/filters.py`).
- OpenAPI: code frequently annotates endpoints using `drf_spectacular.utils.extend_schema` and `OpenApiParameter`. Use these annotations when adding or updating endpoints so schemas remain accurate.
- Admin URL: admin path is intentionally obfuscated in `rexgold/urls.py` (e.g., `WXufeuLAUvDthfLDXtQVNkEKN/`). When adding admin changes, update that route cautiously.

## Integration points & dependencies
- Redis: used for caching, Celery, and Channels (configured in `settings.py`). Default host: `127.0.0.1:6379`.
- Celery: configured; check `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` in `settings.py`.
- Database: default is SQLite3 at `BASE_DIR / 'db.sqlite3'`. Migrations exist per-app.
- Third-party libraries to be aware of (see `requirements.txt`): Django 5.x, DRF, drf-spectacular, simple-jwt, django-redis, celery, channels packages.

## Where to look for common tasks
- Add a new API endpoint: create/update `serializers.py`, `views.py` (prefer `viewsets` if CRUD), and `urls.py` in the app directory. Register app URL in `rexgold/urls.py`.
- Add filters: put a `filters.py` in the app and reference it with `filterset_class` + `DjangoFilterBackend`.
- Authentication checks: use DRF permission classes. There are placeholders like `# permission_classes = [IsAdminUser]` in admin views — follow the existing pattern.

## Examples from the codebase (copyable patterns)
- Factor number generation pattern (see `Order_Module/views.py` AdminAddOrderView):
  - Prefix = `NL-{YYMMDD}-`; sequence is extracted from last `factor_number` and incremented; format `seq:03d`.
- Serializer usage (AdminAddOrderView): validate serializer, then use `validated_data` fields and create model instances.

## Quick notes for an AI agent
- Prefer small, local changes and run tests locally. The repository uses Django's test runner.
- Don't alter `SECRET_KEY` or `DEBUG=True` lines unless explicitly asked; these were committed for development but should remain untouched unless performing a security/ops task.
- When modifying endpoints, update or add `extend_schema` annotations so API docs remain consistent.
- Respect the custom `AUTH_USER_MODEL` (`Account_Module.User`) when creating or querying users.

## Files to inspect for deeper context
- `rexgold/settings.py` — core configuration (auth model, Redis, Celery, DRF settings).
- `rexgold/urls.py` — how apps are mounted and admin path.
- `requirements.txt`, `Dockerfile`, `docker-compose.yml` — run/build workflows.
- Example app: `Order_Module/views.py`, `Order_Module/serializers.py`, `Order_Module/filters.py`.
- `Account_Module/models.py` — custom user details and fields.

If any section is unclear or you'd like more examples (e.g., a sample PR for adding CRUD endpoints), tell me which area to expand and I will iterate.
