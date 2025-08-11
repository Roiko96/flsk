# wsgi.py – כניסה ל-Gunicorn
try:
    from application import app as application  # * ייבוא מהקובץ הראשי
except Exception:
    from app import app as application          # * גיבוי לשמות אחרים
