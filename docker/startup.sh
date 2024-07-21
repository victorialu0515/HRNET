#!/bin/sh

echo Running startup script: $STARTUP_SH

echo Moving to $WORKING_DIR
cd $WORKING_DIR

# Create torch symlink
ln -s $PYTORCH_CACHE_DIR /root/.cache/torch/

tail -f /dev/null
