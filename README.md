# Game Scoreboard – HA (2 instances) on Elastic Beanstalk / us-east-1

- סביבה אחת ב-EB עם **2 אינסטנסים** מאחורי **ALB** (failover ע"י elastic).
- תיוג אינסטנסים: **main**, **main2_HA**.
- פתיחת **all tcp inbound**  ב-SG של ה-ALB ושל האינסטנסים.
- קונטיינר **ubuntu 22.04** עם Flask+Gunicorn על פורט 5000.

> ALL tcp פתוח ל-0.0.0.0/0 הוא לצורכי דמו בלבד. לפרודקשן להגביל ל-80/443/טווחים סגורים.

## הפעלה (Cloud9 / AWS Academy)
```bash
# 1) משיכה וכניסה לתיקייה
git clone https://github.com/roiko96/flsk.git
cd flsk

# 2) קרדנצ'יאלס זמניים מה-Canvas (IAM שהמורה פותח)
export AWS_ACCESS_KEY_ID="PASTE"
export AWS_SECRET_ACCESS_KEY="PASTE"
export AWS_SESSION_TOKEN="PASTE"
export AWS_DEFAULT_REGION="us-east-1"
aws sts get-caller-identity

# 3) יצירת תיקיות/העתקת קבצים למקומם (בטוח להרצה)
mkdir -p templates
[ -f index.html ] && mv -f index.html templates/index.html
[ -f wsgi.py ] || echo 'from application import app as application' > wsgi.py

# 4) הרצה (ללא sudo)
chmod +x deploy_eb.sh
./deploy_eb.sh
