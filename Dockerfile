FROM python:latest

WORKDIR /socialnetwork_api

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r /socialnetwork_api/requirements.txt

COPY . .

ENTRYPOINT ["python",  "./main.py"]