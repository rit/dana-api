pytest:
	YARGS_ENV=test pytest --cov-report term-missing --cov=dana tests

db-up:
	alembic upgrade head

db-down:
	alembic downgrade -1

db-both: db-up db-down

genctags:
	ctags -R --extra=+f dana tests

format:
	yapf -ri dana tests

lint:
	pylint -j 2 dana tests

trim:
	@@find dana -name "*.py" | xargs sed -i '' -e 's/[[:space:]]*$$//'

clear:
	find dana -name '*.pyc' | xargs rm
	find dana -name '__pycache__' | xargs rm -rf

import:
# Start a parallel job for every 500 lines of input from find
	find iiif -type f -name '*.json' | parallel --pipe -N500 python -m dana.loader

import_series:
	find iiif -type f -name '*.json' | python -m dana.loader
	
rsync-output:
	rsync -ruvz output/ ~/repo/dana.git/static

backup-dev-db:
	pg_dump -Fc --no-acl --no-owner dana_api_dev > dana_api_dev.dump

danapy_image:
	docker build --rm -t danapy:v0.3.2 .

nginx_image:
	docker build -f Dockerfile.nginx --rm -t dana-nginx:v0.3.2 .

docker_images: danapy_image nginx_image

push_iiif__to_dana_qa:
	rsync -ruz iiif dana-qa:/var/dana/dana-api
