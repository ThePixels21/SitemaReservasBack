deploy:
	@docker compose build
	@docker compose up -d
	@sleep 10
	@docker cp backend:/app/alembic/versions ./FastAPI/app/alembic
