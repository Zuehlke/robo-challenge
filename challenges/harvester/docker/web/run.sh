#!/bin/bash

PORT="8080"

echo "starting web server on port $PORT"
docker run --rm -p $PORT:80 robot/web