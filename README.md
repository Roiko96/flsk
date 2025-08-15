# game scoreboard – docker on ec2 via cloudformation

- autoscaling group (min=2, desired=2, max=2). if one ec2 dies, asg launches a new one.
- english index. container on port 5000. health: /healthz.
- no beanstalk. cloudformation only. run from cloud9.

## run (cloud9)
```

git clone https://github.com/roiko96/flsk.git
cd flsk

export AWS_DEFAULT_REGION=us-east-1
aws sts get-caller-identity
sudo apt update && sudo apt upgrade -y
sudo apt install python3-flask -y
python3 application.py
```
# destroy 
```
aws cloudformation delete-stack --stack-name flsk-ec2
aws cloudformation wait stack-delete-complete --stack-name flsk-ec2
```
![Uploading image.png…]()
