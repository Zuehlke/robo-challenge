#!/bin/bash

DOCKER_CONTENT_DIR="docker_content"

echo "create $DOCKER_CONTENT_DIR dir"
rm -rf $DOCKER_CONTENT_DIR
mkdir $DOCKER_CONTENT_DIR


echo "copy content to $DOCKER_CONTENT_DIR dir"
cp -R ./../../ui/* $DOCKER_CONTENT_DIR/

echo "build image"
docker build -t robot/web .