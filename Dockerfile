FROM python:3.11-slim

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
ENTRYPOINT ["/bin/sh", "-c"]
CMD ["gunicorn --workers 2 --bind 0.0.0.0:8080 --access-logfile - service:app"]
