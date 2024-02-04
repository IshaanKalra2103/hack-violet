# FROM python:3.9-slim-buster
FROM gcr.io/gomama-413222/hackviolet-api:latest

COPY . /api

WORKDIR /api

RUN pip install --no-cache-dir -r requirements.txt

RUN pip list

EXPOSE 8080

# CMD exec gunicorn --bind :8080 --workers 8 --threads 8 app:iface
CMD ["python3", "app.py"]