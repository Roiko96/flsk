#!/usr/bin/env bash
set -euo pipefail

REGION="us-east-1"              # * אזור
APP="game-scoreboard-app"       # * שם אפליקציה
ENV="game-scoreboard-env"       # * שם סביבה
PLAT1='Docker running on 64bit Amazon Linux 2023'
PLAT2='Docker running on 64bit Amazon Linux 2'

echo "[1/5] אימות AWS בסביבת הלמידה (Cloud9 כבר מחובר)..."
aws sts get-caller-identity >/dev/null

echo "[2/5] התקנת EB CLI (אם צריך)..."
if ! command -v eb >/dev/null 2>&1; then
  pip3 install --user --upgrade awsebcli
  export PATH="$HOME/.local/bin:$PATH"
fi

echo "[3/5] EB init..."
if [[ ! -f .elasticbeanstalk/config.yml ]]; then
  (printf "n\n") | eb init -p "$PLAT1" "$APP" --region "$REGION" || \
  (printf "n\n") | eb init -p "$PLAT2" "$APP" --region "$REGION"
else
  echo "config.yml קיים - דילוג על init"
fi

echo "[4/5] יצירת/עדכון סביבה (ALB + Multi-AZ)..."
if eb list 2>/dev/null | grep -qx "$ENV"; then
  eb deploy "$ENV"
else
  eb create "$ENV" --elb-type application --scale 2 --region "$REGION"
fi

echo "[5/5] המתנה ל-Green והדפסת ה-URL היציב..."
for i in {1..30}; do
  STATUS=$(eb status "$ENV" | awk -F': ' '/Status/{print $2}')
  HEALTH=$(eb status "$ENV" | awk -F': ' '/Health/{print $2}')
  echo "Status: $STATUS | Health: $HEALTH"
  [[ "$HEALTH" == "Green" ]] && break
  sleep 20
done

CNAME=$(eb status "$ENV" | awk -F': ' '/CNAME/{print $2}')
echo "============================================================"
echo "App URL (יציב מאחורי ALB):  http://$CNAME"
echo "============================================================"
