#!/bin/bash
set -e

echo "Initializing Elastic Beanstalk..."
eb init -p python-3.8 game-scoreboard-ha --region us-east-1 --platform "Docker"
eb create game-scoreboard-env
eb open