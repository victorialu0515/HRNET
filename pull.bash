# authentication with AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 970557581191.dkr.ecr.us-east-1.amazonaws.com

# Pull base image
docker pull 970557581191.dkr.ecr.us-east-1.amazonaws.com/hrnet