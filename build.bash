#!/bin/bash

echo "Building docker image"
docker build -t 970557581191.dkr.ecr.us-east-1.amazonaws.com/hrnet -f docker/Dockerfile .
