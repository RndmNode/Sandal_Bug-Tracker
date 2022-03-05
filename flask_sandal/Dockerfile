# syntax=docker/dockerfile:1.3

FROM python:3.9-slim-bullseye

WORKDIR /Users/tzeller/Sandbox/Sandal/flask_sandal

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]