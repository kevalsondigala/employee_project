# Employee Django Challenge (3-hour prototype)

## Quick start (local)
1. Copy `.env.example` to `.env` and adjust DATABASE_URL.
2. Create virtualenv:
   python -m venv venv && source venv/bin/activate
3. Install:
   pip install -r requirements.txt
4. Run migrations:
   python manage.py migrate
5. Create superuser:
   python manage.py createsuperuser
6. Generate seed data:
   python manage.py generate_seed
7. Run server:
   python manage.py runserver
8. Open Swagger UI: http://127.0.0.1:8000/swagger/

## Docker
docker-compose up --build

## Endpoints
- `/api/employees/` (GET/POST) — supports search & ordering & pagination
- `/api/analytics/` — aggregate numbers for visualization
- `/api/export/employees/` — CSV export
- `/health/` — health check
- `/swagger/` — API docs

## Notes
- Token auth enabled. Use DRF token auth or session auth for quick testing.
- Throttling set: anon 20/min, user 100/min.
