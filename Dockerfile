FROM python:3.13-slim

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:8080", "--access-logfile", "-", "--graceful-timeout", "30", "--timeout", "30", "service:app"]
