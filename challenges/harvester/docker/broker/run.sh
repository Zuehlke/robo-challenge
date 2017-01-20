#!/bin/bash

PORT=1883
WEBSOCKET=9001

echo "starting broker on port $PORT / $WEBSOCKET"
docker run --rm -ti -p $PORT:1883 -p $WEBSOCKET:9001 --name broker toke/mosquitto