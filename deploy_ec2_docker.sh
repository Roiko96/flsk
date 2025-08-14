#!/usr/bin/env bash
set -euo pipefail

REGION="us-east-1"    # שנה אם צריך
KEY_NAME="ec2-docker-key"
SEC_GROUP="ec2-docker-sg"

echo "[1/5] יצירת מפתח SSH..."
aws ec2 create-key-pair \
  --key-name "$KEY_NAME" \
  --query 'KeyMaterial' \
  --region "$REGION" \
  --output text > ${KEY_NAME}.pem
chmod 400 ${KEY_NAME}.pem

echo "[2/5] יצירת Security Group..."
SG_ID=$(aws ec2 create-security-group \
  --group-name "$SEC_GROUP" \
  --description "Allow SSH and 5000" \
  --region "$REGION" \
  --query 'GroupId' \
  --output text)

aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0 --region "$REGION"
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 5000 --cidr 0.0.0.0/0 --region "$REGION"

echo "[3/5] הרצת אינסטנס EC2..."

# בחירת ה-AMI החדש ביותר של Ubuntu 22.04
AMI_ID=$(aws ec2 describe-images \
  --owners amazon \
  --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
            "Name=state,Values=available" \
  --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
  --region "$REGION" \
  --output text)

INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --count 1 \
  --instance-type t2.micro \
  --key-name "$KEY_NAME" \
  --security-group-ids "$SG_ID" \
  --region "$REGION" \
  --query 'Instances[0].InstanceId' \
  --output text)

echo "ממתין ל-EC2..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID" --region "$REGION"

PUBLIC_IP=$(aws ec2 describe-instances \
  --instance-ids "$INSTANCE_ID" \
  --region "$REGION" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' \
  --output text)

echo "[4/5] התקנת Docker ופריסת האפליקציה..."
ssh -o StrictHostKeyChecking=no -i ${KEY_NAME}.pem ubuntu@$PUBLIC_IP << 'EOF'
  sudo apt-get update -y
  sudo apt-get install -y docker.io git
  sudo systemctl start docker
  sudo systemctl enable docker
  git clone https://github.com/roiko96/flsk
  cd flsk
  sudo docker build -t flask-app .
  sudo docker run -d -p 5000:5000 flask-app
EOF

echo "[5/5] האתר מוכן!"
echo "פתח בדפדפן: http://$PUBLIC_IP:5000"
