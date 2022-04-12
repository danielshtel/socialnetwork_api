#
FROM python:latest

#
WORKDIR /socialnetwork_api

#
COPY ./requirements.txt /socialnetwork_api/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /socialnetwork_api/requirements.txt
COPY . .

#
EXPOSE 8282
