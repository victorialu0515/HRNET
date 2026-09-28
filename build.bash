#!/bin/bash

echo "Building docker image"
docker build --platform linux/amd64 -t 339713152729.dkr.ecr.us-east-2.amazonaws.com/hrnet -f docker/Dockerfile .
