#!/bin/bash

echo "Building docker image"
docker build -t 339713152729.dkr.ecr.us-east-2.amazonaws.com/hrnet -f docker/Dockerfile .
