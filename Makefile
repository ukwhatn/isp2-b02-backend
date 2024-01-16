build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

reset:
	docker compose down --volumes --remove-orphans

ps:
	docker compose ps

log:
	docker compose logs -f

revision:
	docker compose exec server /bin/bash -c "cd /db && alembic revision --autogenerate -m '${NAME}'"

migrate:
	docker compose exec server /bin/bash -c "cd /db && alembic upgrade head"

init:
	cp envs/db.env.sample envs/db.env
	cp envs/server.env.sample envs/server.env
	make up
	make migrate
