Setup the dev environment:
==========================

Prerequisites:
--------------

Install:

- pip_
- docker_


Build dana-api Docker images:
-----------------------------

Run::

  make danapy_image


Start the api server:
---------------------

Run::

  docker-compose up -d
  docker-compose start api


Load iiif data into the Postgres
--------------------------------

First::


  docker-compose run api alembic upgrade head


Extract IIIF json data into the directry called `iiif`, we need to generate a
text file which lists the full path name of each of the json document::


  find iiif -type f -name '*.json' > jsons.txt


We can then make use the jsons.txt like this::

  docker-compose run api python -m dana.loader jsons.txt


To test the API, open this url in the browser: http://localhost:5000/collections/2011m30


Mirador for DANA
----------------

We need a patched version of mirador that supports ajax headers.

Clone the repo::

  git clone -b danazen https://github.com/rit/mirador.git


Then create a symblink::

  ln -s path/mirador/repo mirador


Troubleshooting:
----------------

Run::

  docker-compose ps

The output should look similar to this::

  Name                    Command               State           Ports
  ----------------------------------------------------------------------------------
  danaapigit_api_1   python -m flask run --host ...   Up      0.0.0.0:5000->5000/tcp
  danaapigit_db_1    docker-entrypoint.sh postgres    Up      5432/tcp


If the States are not `Up`, run this command::

  docker-compose start api


.. _pip: https://pip.pypa.io/en/stable/installing/#installing-with-get-pip-py
.. _docker: https://www.docker.com/community-edition#/download
