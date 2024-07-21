# authentication with AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 970557581191.dkr.ecr.us-east-1.amazonaws.com

# create a new repository in ECR
aws ecr create-repository \
    --repository-name hrnet \
    --region us-east-1

# push the image to ECR
docker push 970557581191.dkr.ecr.us-east-1.amazonaws.com/hrnet
