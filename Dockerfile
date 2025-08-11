FROM python:3.12-slim                # * בסיס פייתון קליל
WORKDIR /app                         # * תיקיית עבודה
ENV PYTHONDONTWRITEBYTECODE=1        # * לא לכתוב pyc
ENV PYTHONUNBUFFERED=1               # * לוגים חיים
COPY requirements.txt .              # * תלויות
RUN pip install --no-cache-dir -r requirements.txt
COPY . .                             # * קוד
EXPOSE 5000                          # * חשיפת פורט בקונטיינר
CMD ["gunicorn","-w","2","-b","0.0.0.0:5000","wsgi:application"]  # * שרת
