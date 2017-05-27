db-up:
	PYTHONPATH=. alembic upgrade head

db-down:
	PYTHONPATH=. alembic downgrade -1

db-both: db-up db-down

trim:
	@@find dana -name "*.py" | xargs sed -i '' -e 's/[[:space:]]*$$//'

import:
# Start a parallel job for every 500 lines of input from find
	find iiif -type f -name '*.json' | parallel --pipe -N500 python -m dana.walker
