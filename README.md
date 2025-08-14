# Game Scoreboard – HA (2 instances) on Elastic Beanstalk / us-east-1

- שני אינסטנסים מאחורי ALB באותה סביבה (EB) – **main** ו‑**main2_HA** (תיוג אוטומטי).
- פתיחת **ALL TCP inbound** ל‑SG של ה‑ALB ושל האינסטנסים (דמו).
- רץ מ‑Cloud9 (AWS Academy).

## הפעלה (Cloud9)
```
git clone https://github.com/roiko96/flsk.git
cd flsk

# קרדנצ'יאלס זמניים מה-Canvas
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_SESSION_TOKEN=""
export AWS_DEFAULT_REGION="us-east-1"

aws sts get-caller-identity

# סידור תקיות (בטוח להרצה)
mkdir -p templates
[ -f index.html ] && mv -f index.html templates/index.html
[ -f wsgi.py ] || echo 'from application import app as application' > wsgi.py

# הרצה (ללא sudo)
chmod +x deploy_eb.sh
./deploy_eb.sh
