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
```
# troubleshoot : 

```

# eb cli not found 
python3 -m pip install --user --upgrade awsebcli && export PATH="$HOME/.local/bin:$PATH" && eb --version

# follow events + grab logs (errors only)
eb events --follow --region us-east-1 --environment main
eb logs --all   --region us-east-1 --environment main | egrep -i 'error|traceback|gunicorn' | tail -n 120

# check cname + health
CNAME=$(aws elasticbeanstalk describe-environments --region us-east-1 \
  --application-name game-scoreboard-app --environment-names main \
  --query 'Environments[0].CNAME' --output text)

curl -s -o /dev/null -w "%{http_code}\n" "http://${CNAME}/healthz"   # expect: 200

# invalid/expired token?
aws sts get-caller-identity || echo "re-export credentials from canvas"

# platform not found?
echo 'platform must be: Docker running on 64bit Amazon Linux 2023'
```
# redeploy if neccesery: 
```
(printf "n\n") | eb init -p "Docker running on 64bit Amazon Linux 2023" game-scoreboard-app --region us-east-1
eb deploy main
```

# destroy env 
```
# delete environment (keeps the application)
eb terminate main --force --region us-east-1

# optional: delete the EB application itself (after env is gone)
aws elasticbeanstalk delete-application \
  --application-name game-scoreboard-app \
  --terminate-env-by-force \
  --region us-east-1
```
*enjoy*


