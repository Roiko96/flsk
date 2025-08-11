#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] התקנת תלויות להרצה לוקלית..."
pip3 install --user -r requirements.txt

echo "[2/4] זיהוי אינסטנס ו-SG..."
IID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id)
REGION="us-east-1"
SG=$(aws ec2 describe-instances --region "$REGION" --instance-ids "$IID" \
     --query "Reservations[0].Instances[0].SecurityGroups[0].GroupId" --output text)

echo "[3/4] פתיחת פורט 5000 ב-SG..."
set +e
aws ec2 authorize-security-group-ingress --region "$REGION" \
  --group-id "$SG" --protocol tcp --port 5000 --cidr 0.0.0.0/0 2>/dev/null
set -e

echo "[4/4] הרצת Flask על 0.0.0.0:5000..."
python3 application.py > app.log 2>&1 &
PUBIP=$(curl -s http://checkip.amazonaws.com)
echo "============================================================"
echo "Local EC2 URL (לא HA):  http://$PUBIP:5000"
echo "============================================================"
