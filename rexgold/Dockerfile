# استفاده از پایتون سبک
FROM python:3.11-slim

# تنظیمات محیطی
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# دایرکتوری کاری
WORKDIR /app

# کپی و نصب پکیج‌ها
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# کپی کل پروژه
COPY . .

# پورت 8000
EXPOSE 8000

# اجرای سرور توسعه
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]