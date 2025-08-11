
** myapp01

```markdown
# Game Scoreboard – Flask (by roiko)

אפליקציית Flask קטנה שמנהלת ניקוד משחקים בזיכרון (ללא DB):
הוספה/מחיקה/עריכה/מיון/ממוצע. דף HTML פשוט עם Bootstrap.

## פריסה מהירה ב‑AWS (Elastic Beanstalk + HA)

```
sudo apt-get update -y
pip3 install --user --upgrade awsebcli
export PATH=$PATH:$HOME/.local/bin

cd ~
rm -rf flsk
git clone https://github.com/Roiko96/flsk.git
cd flsk

eb init -p docker "game-scoreboard" --region us-east-1
eb create gs-ha --elb-type application --cname $(whoami)-gs --scale 2
eb open
