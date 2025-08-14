# Game scoreboard – Flask + Docker (Ubuntu 22.04) on Elastic Beanstalk

פרויקט דמו עם Flask בתוך קונטיינר **ubuntu:22.04**, פריסה ל‑**Elastic Beanstalk**:
- ראשי: **us-east-1** (ALB + שתי מכונות)
- DR: **us-west-1**
- פקודה אחת שמקימה ומדפיסה כתובות.

## הרצה מ‑0 על Cloud9

```bash
# 1) clone של הפרויקט
git clone https://github.com/roiko96/flsk
cd flsk

# 2) export לקרדנצ'יאלס מה‑Canvas (AWS Academy)
export AWS_ACCESS_KEY_ID="PASTE"
export AWS_SECRET_ACCESS_KEY="PASTE"
export AWS_SESSION_TOKEN="PASTE"
export AWS_DEFAULT_REGION="us-east-1"
aws sts get-caller-identity

# 3) הקמה
chmod +x deploy_eb.sh
./deploy_eb.sh
