FROM python:2

# ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
# RUN pip install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ADD . /code/
