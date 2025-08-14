#!/usr/bin/env bash
set -euo pipefail

# ===== הגדרות =====
REGION="us-east-1"              # שנה ל-region שלך אם צריך (למשל us-west-2)
APP="game-scoreboard-app"
ENV="game-scoreboard-env"
PLAT1='Docker running on 64bit Amazon Linux 2023'
PLAT2='Docker running on 64bit Amazon Linux 2'

echo "============================================================"
echo " Game Scoreboard - Full Auto Deployment"
echo "============================================================"

echo "[1/7] אימות AWS..."
if ! aws sts get-caller-identity >/dev/null 2>&1; then
  echo " AWS credentials לא טעונים. ודא שאתה ב-Cloud9 עם חיבור ל-AWS Academy."
  exit 1
fi

echo "[2/7] בדיקת הרשאות ל-Elastic Beanstalk באזור $REGION..."
if ! aws elasticbeanstalk list-available-solution-stacks --region "$REGION" >/dev/null 2>&1; then
  echo " אין הרשאה ל-EB ב-$REGION. נסה אזור אחר או פנה למדריך."
  exit 1
fi

echo "[3/7] בדיקת Docker ו-Python..."
sudo apt-get update -y
sudo apt-get install -y docker.io python3 python3-pip ca-certificates
sudo systemctl enable docker
sudo systemctl start docker

echo "[4/7] התקנת ספריות Python..."
pip3 install --upgrade pip
pip3 install --no-cache-dir -r requirements.txt

echo "[5/7] התקנת EB CLI..."
if ! command -v eb >/dev/null 2>&1; then
  pip3 install --user --upgrade awsebcli
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "[6/7] EB init (ללא CodeCommit)..."
if [[ ! -f .elasticbeanstalk/config.yml ]]; then
  yes "n" | eb init -p "$PLAT1" "$APP" --region "$REGION" || \
  yes "n" | eb init -p "$PLAT2" "$APP" --region "$REGION"
else
  echo "config.yml קיים - דילוג על init"
fi

echo "[7/7] יצירת/עדכון סביבה עם HA..."
if eb list 2>/dev/null | grep -qx "$ENV"; then
  echo " מבצע deploy לסביבה קיימת..."
  eb deploy "$ENV"
else
  echo " יוצר סביבה חדשה עם Auto Scaling (2-4 אינסטנסים, Multi-AZ)"
  eb create "$ENV" \
    --elb-type application \
    --scale 2 \
    --region "$REGION"
fi

for i in {1..30}; do
  STATUS=$(eb status "$ENV" | awk -F': ' '/Status/{print $2}')
  HEALTH=$(eb status "$ENV" | awk -F': ' '/Health/{print $2}')
  echo "Status: $STATUS | Health: $HEALTH"
  [[ "$HEALTH" == "Green" ]] && break
  sleep 20
done

CNAME=$(eb status "$ENV" | awk -F': ' '/CNAME/{print $2}')
echo "============================================================"
echo "✅ האפליקציה זמינה בכתובת:  http://$CNAME"
echo "============================================================"
