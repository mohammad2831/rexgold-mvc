# Dockerfile — نسخه حرفه‌ای و بهینه
FROM python:3.11-slim

# تنظیمات محیطی
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DOCKER_ENV=1

# نصب وابستگی‌های سیستمی
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# دایرکتوری کاری
WORKDIR /app

# کپی و نصب پکیج‌ها (اول requirements → بهتر کش می‌شه)
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# کپی پروژه
COPY . .

# پورت
EXPOSE 8000

# استفاده از gunicorn در تولید (runserver فقط برای توسعه)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]