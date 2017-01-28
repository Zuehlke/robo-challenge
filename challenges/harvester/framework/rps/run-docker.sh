#!/bin/bash

docker run -v ${PWD}:/notebooks --device=/dev/video0 -p8888:8888 -it fluescher/opencv $1
