# انتخاب نسخه پایتون (سبک)
FROM python:3.11-slim

# جلوگیری از تولید pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# پوشه کاری داخل کانتینر
WORKDIR /app

# کپی کردن فایل‌های مورد نیاز
COPY requirements.txt .

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کل پروژه
COPY . .

# اجرای برنامه
CMD ["python", "bot.py"]