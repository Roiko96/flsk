# Game scoreboard – Flask app + Docker (Ubuntu 22.04) on Elastic Beanstalk

פרויקט הדגמה עם Flask, קונטיינר **ubuntu:22.04**, פריסה ל‑**Elastic Beanstalk**:
- סביבה ראשית: **us-east-1** (HA – שתי מכונות מאחורי ALB)
- סביבת DR: **us-west-1**
- פקודה אחת שמקימה הכל ומדפיסה כתובות.

## הרצה מ-0 על Cloud9

```bash
# 1) clone של הפרויקט
git clone https://github.com/roiko96/flsk
cd flsk

# 2) export לקרדנצ'יאלס מה-Canvas (AWS Academy)
export AWS_ACCESS_KEY_ID="PASTE"
export AWS_SECRET_ACCESS_KEY="PASTE"
export AWS_SESSION_TOKEN="PASTE"
export AWS_DEFAULT_REGION="us-east-1"
aws sts get-caller-identity

# 3) פקודה אחת שמקימה הכול (מזרח + מערב) ומדפיסה כתובות
chmod +x deploy_eb.sh
./deploy_eb.sh
