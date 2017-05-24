db-up:
	alembic upgrade head

db-down:
	alembic downgrade -1

db-both: db-up db-down

trim:
	@@find dana -name "*.py" | xargs sed -i '' -e 's/[[:space:]]*$$//'
