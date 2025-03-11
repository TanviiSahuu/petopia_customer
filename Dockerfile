# Dockerfile.customer

FROM python:3.9-slim

# Prevent Python from writing .pyc files to disc and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project code
COPY . .

# Expose port 8000 (or the port your Django service listens on)
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
