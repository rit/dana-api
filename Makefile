pytest:
	YARGS_ENV=test pytest --cov-report term-missing --cov=dana dana

db-up:
	alembic upgrade head

db-down:
	alembic downgrade -1

db-both: db-up db-down

trim:
	@@find dana -name "*.py" | xargs sed -i '' -e 's/[[:space:]]*$$//'

import:
# Start a parallel job for every 500 lines of input from find
	find iiif -type f -name '*.json' | parallel --pipe -N500 python -m dana.walker

import_series:
	find iiif -type f -name '*.json' | python -m dana.walker
	
rsync-output:
	rsync -ruvz output/ ~/repo/dana.git/static
