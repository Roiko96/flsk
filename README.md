# game scoreboard – docker on ec2/alb via cloudformation

- alb + autoscaling group (min=2, desired=2, max=2). if one ec2 dies, asg launches a new one.
- english index. container on port 5000. health: /healthz.
- no beanstalk. cloudformation only. run from cloud9.

## run (cloud9)
```bash
# 0) clone + cd
git clone https://github.com/roiko96/flsk.git
cd flsk

# 1) make sure template exists
ls cfn/app.yml

# 2) region + identity
export AWS_DEFAULT_REGION=us-east-1
aws sts get-caller-identity

# 3) default vpc + public subnets (comma-separated)
VPC_ID=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text)
SUBNETS=$(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC_ID Name=default-for-az,Values=true --query 'Subnets[].SubnetId' --output text | tr '\t' ',')
echo "$VPC_ID"
echo "$SUBNETS"

# 4) deploy cloudformation (alb + asg + docker build on each node)
aws cloudformation deploy \
  --stack-name flsk-ec2 \
  --template-file cfn/app.yml \
  --parameter-overrides \
    VpcId="$VPC_ID" \
    PublicSubnets="$SUBNETS" \
    InstanceType=t3.micro \
    MinSize=2 DesiredCapacity=2 MaxSize=2 \
    OpenAllTcp=true \
    GitRepoUrl="https://github.com/roiko96/flsk.git" \
    GitBranch="main"

# 5) get url + health (expect 200)
URL=$(aws cloudformation describe-stacks --stack-name flsk-ec2 \
  --query "Stacks[0].Outputs[?OutputKey=='LoadBalancerDNS'].OutputValue" --output text)
echo "url: $URL"
curl -s -o /dev/null -w "%{http_code}\n" "$URL/healthz"
