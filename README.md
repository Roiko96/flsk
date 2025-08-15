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
sudo apt install python3-flask
python3 application.py
```
