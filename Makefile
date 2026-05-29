.PHONY: up down logs backend-shell frontend-shell

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

backend-shell:
	docker compose exec backend /bin/sh

frontend-shell:
	docker compose exec frontend /bin/sh
