#!/bin/bash
# 2023-3-2 by Xuan
echo ">>> Building lipdub docker image..."

# Pull base image
echo "Pulling base docker image"
docker pull harbor.marz.vfx/ml/nvidia/cuda:12.1.0-cudnn8-devel-ubuntu20.04

pubkey=$(ssh-add -l 2>&1 )

if [[ "$pubkey" == "The agent has no identities." ]]; then
    ssh-add

elif [[ "$pubkey" == "Could not open a connection to your authentication agent." ]]; then
    echo "load key into new agent"
    eval $(ssh-agent)
    echo "Please enter the path to your SSH key (or press Enter to use the default path ~/.ssh/id_ed25519):"
    read ssh_key_path

    if [ -z "$ssh_key_path" ]; then
	    eval ssh-add "~/.ssh/id_ed25519"
    else
        eval ssh-add "$ssh_key_path"
    fi

fi

# Build docker image
echo "Building lipdub docker image"

DOCKER_BUILDKIT=1 docker build --ssh default=$SSH_AUTH_SOCK -t harbor.marz.vfx/ml/lipdub -f docker/lipdub.dockerfile .
