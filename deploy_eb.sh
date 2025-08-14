#!/usr/bin/env bash
set -Eeuo pipefail

APP="game-scoreboard-app"
ENV="main"                 # שם סביבת EB
REGION="us-east-1"
PLATFORM="Docker running on 64bit Amazon Linux 2023"

green(){ printf "\033[1;32m==> %s\033[0m\n" "$*"; }
note(){ printf "\033[1;34m[i]\033[0m %s\n" "$*"; }
die(){ printf "\033[1;31m[ERROR]\033[0m %s\n" "$*" >&2; exit 1; }

# 0) בדיקות בסיס
command -v aws >/dev/null || die "aws cli לא זמין"
[[ -n "${AWS_ACCESS_KEY_ID:-}" && -n "${AWS_SECRET_ACCESS_KEY:-}" && -n "${AWS_SESSION_TOKEN:-}" ]] \
  || die "חסרים AWS_* מה-Canvas (ACCESS/SECRET/SESSION_TOKEN)."
aws sts get-caller-identity >/dev/null || die "קרדנצ'יאלס לא תקינים/פגו."

# 1) EB CLI
export PATH="$HOME/.local/bin:$PATH"
command -v eb >/dev/null || python3 -m pip install --user --upgrade awsebcli >/dev/null
command -v eb >/dev/null || die "EB CLI לא הותקן. נסה שוב: python3 -m pip install --user awsebcli"
green "EB CLI: $(eb --version)"

# 2) סידור תקיות וקבצים (בטוח להרצה)
mkdir -p templates
[ -f index.html ] && mv -f index.html templates/index.html
[ -f wsgi.py ] || echo 'from application import app as application' > wsgi.py
grep -q '^Flask' requirements.txt 2>/dev/null || echo 'Flask>=2.3,<4' >> requirements.txt
grep -q '^gunicorn' requirements.txt 2>/dev/null || echo 'gunicorn>=21,<23' >> requirements.txt
sed -i 's/\r$//' deploy_eb.sh 2>/dev/null || true  # מנקה CRLF אם צריך

# 3) EB init + create (ALB + שני אינסטנסים)
rm -rf .elasticbeanstalk
(printf "n\n") | eb init -p "$PLATFORM" "$APP" --region "$REGION"
green "מקימים סביבה '$ENV' עם ALB ו-scale=2..."
eb create "$ENV" --platform "$PLATFORM" --elb-type application --scale 2 --region "$REGION"

# 4) המתנה ל-Green + שליפת CNAME
green "ממתין ל-Green..."
for i in {1..60}; do
  H=$(aws elasticbeanstalk describe-environments --region "$REGION" --application-name "$APP" \
       --environment-names "$ENV" --query 'Environments[0].Health' --output text 2>/dev/null || echo "Unknown")
  echo "Health: $H"
  [ "$H" = "Green" ] && break
  sleep 10
done
CNAME=$(aws elasticbeanstalk describe-environments --region "$REGION" --application-name "$APP" \
        --environment-names "$ENV" --query "Environments[0].CNAME" --output text)
URL="http://${CNAME}"
green "URL: $URL"

# 5) פתיחת ALL TCP (0-65535) ב-SG של ה-LB ושל האינסטנסים
green "פותח ALL TCP ב-SG של ה-ALB ושל האינסטנסים (ייתכן שכבר פתוח; נתעלם משגיאת Duplicate)."

# --- LB SG ---
LB_NAME=$(aws elasticbeanstalk describe-environment-resources --environment-name "$ENV" --region "$REGION" \
          --query 'EnvironmentResources.LoadBalancers[0].Name' --output text)
LB_SGS=$(aws elbv2 describe-load-balancers --names "$LB_NAME" --region "$REGION" \
         --query 'LoadBalancers[0].SecurityGroups' --output text)
for sg in $LB_SGS; do
  aws ec2 authorize-security-group-ingress --region "$REGION" \
    --group-id "$sg" --ip-permissions IpProtocol=tcp,FromPort=0,ToPort=65535,IpRanges='[{CidrIp=0.0.0.0/0,Description="open all tcp (demo)"}]' \
    >/dev/null 2>&1 || true
done

# --- Instance SG(s) ---
INST_IDS=$(aws elasticbeanstalk describe-environment-resources --environment-name "$ENV" --region "$REGION" \
           --query 'EnvironmentResources.Instances[].Id' --output text)
if [ -n "$INST_IDS" ]; then
  INST_SGS=$(aws ec2 describe-instances --region "$REGION" --instance-ids $INST_IDS \
             --query 'Reservations[].Instances[].SecurityGroups[].GroupId' --output text | tr '\t' '\n' | sort -u)
  for sg in $INST_SGS; do
    aws ec2 authorize-security-group-ingress --region "$REGION" \
      --group-id "$sg" --ip-permissions IpProtocol=tcp,FromPort=0,ToPort=65535,IpRanges='[{CidrIp=0.0.0.0/0,Description="open all tcp (demo)"}]' \
      >/dev/null 2>&1 || true
  done
fi

# 6) תיוג האינסטנסים: main, main2_HA
read -r I1 I2 <<<"$INST_IDS"
[ -n "${I1:-}" ] && aws ec2 create-tags --region "$REGION" --resources "$I1" --tags Key=Name,Value=main >/dev/null 2>&1 || true
[ -n "${I2:-}" ] && aws ec2 create-tags --region "$REGION" --resources "$I2" --tags Key=Name,Value=main2_HA >/dev/null 2>&1 || true
note "תיוג בוצע (אם סדר שונה – לא קריטי)."

cat <<TXT

============================================================
מוכן!  כתובת: $URL
HA: ALB מפנה בין שני אינסטנסים. אם אחד נופל, השני ממשיך לשרת.
SG: נפתח ALL TCP (demo) גם ל-ALB וגם לאינסטנסים.
לוגים:    eb logs --all
אירועים:  eb events --follow
סקייל:    eb scale 2
============================================================
TXT
