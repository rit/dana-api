db-up:
	PYTHONPATH=. alembic upgrade head

db-down:
	PYTHONPATH=. alembic downgrade -1

db-both: db-up db-down

trim:
	@@find dana -name "*.py" | xargs sed -i '' -e 's/[[:space:]]*$$//'
