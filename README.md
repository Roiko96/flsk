# Game scoreboard – flask app+ Docker (ubuntu 22.04) on elastic beanstalk

פרויקט הדגמה עם Flask, קונטיינר **ubuntu lts 22.04**, פריסה ל‑**elastic Beanstalk**:
- סביבה ראשית: **us-east-1** (HA – 2 AZs מאחורי ALB)
- סביבת DR: **us-west-1**
- פקודה אחת שמקימה הכול ומדפיסה כתובות.

## הרצה מ-0 על Cloud9

```bash
# 1) clone של הפרויקט
git clone https://github.com/roiko96/flsk
cd flsk

# 2) export לקרדשנלס מה- canvas (aws academy)
export AWS_ACCESS_KEY_ID="PASTE"
export AWS_SECRET_ACCESS_KEY="PASTE"
export AWS_SESSION_TOKEN="PASTE"
export AWS_DEFAULT_REGION="us-east-1"
aws sts get-caller-identity

# 3) פקודה אחת שמקימה הכול (בשני ריגנים כמובן.. גם ב us-east-1 וגם ב us-west-1 ) ומדפיסה כתובות
chmod +x deploy_eb.sh
./deploy_eb.sh
