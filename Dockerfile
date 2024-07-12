FROM python:3.11-slim-buster

WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /src

ENTRYPOINT ["python", "/app/codetriage.py"]