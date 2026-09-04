FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY dashboard/ /app/dashboard/

EXPOSE 8000

WORKDIR /app/dashboard
CMD ["python", "server.py"]
