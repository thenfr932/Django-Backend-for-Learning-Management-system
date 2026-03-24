.PHONY: build up down logs restart migrate shell test collectstatic lint clean

# ---- Docker Compose ----
build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

# ---- Django Commands (inside container) ----
migrate:
	docker compose exec web python manage.py migrate

shell:
	docker compose exec web python manage.py shell

test:
	docker compose exec web python manage.py test --verbosity=2

collectstatic:
	docker compose exec web python manage.py collectstatic --noinput

createsuperuser:
	docker compose exec web python manage.py createsuperuser

# ---- Development ----
lint:
	flake8 . --count --max-line-length=120 --statistics

# ---- Cleanup ----
clean:
	docker compose down -v --remove-orphans
	docker image prune -f
