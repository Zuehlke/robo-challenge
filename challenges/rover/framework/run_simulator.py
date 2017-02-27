# -*- coding: utf-8 -*-
import sys
import logging
import json
import getopt
import paho.mqtt.client as mqtt
import time

from simulator import Simulator
from simulator import TimeDecorator
from common import CommandDispatcher

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

TIMEOUT_SEC = 0.15
KEEPALIVE_SEC = 60

START_X = 640
START_Y = 480
ROBOT_R = 15


# default mqtt broker (hostname or ip) and port
server = "broker"
port = 1883


if __name__ == "__main__":

    logging.info("Starting simulator...")

    # parse args
    optlist, args = getopt.getopt(sys.argv[1:], shortopts="", longopts=["broker=", "port="])

    for opt, arg in optlist:
        if opt == '--broker':
            server = arg
        elif opt == '--port':
            port = int(arg)

    robot = TimeDecorator(Simulator(x=START_X, y=START_Y, r=ROBOT_R, angle=0))
    #robot = Simulator(x=game.center_x(), y=game.center_y(), r=15, angle=0)
    logging.info("Robot: " + str(robot))

    dispatcher = CommandDispatcher(robot)

    logging.info("Try to connect to " + str(server) + ":" + str(port))

    client = mqtt.Client()
    client.connect(server, port, KEEPALIVE_SEC)


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        logging.info("Connected with return code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("robot/process")


    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        logging.info("Received message '" + str(msg.payload) + " on topic " + msg.topic + " with QoS " + str(msg.qos))

        if "robot" in msg.topic:
            try:
                obj = json.loads(msg.payload.decode('utf-8'))
                dispatcher.exec(obj)
            except Exception as ex:
                logging.exception("Invalid message format! %s" % msg.payload)
                client.publish("robot/error",  json.dumps({'type': type(ex).__name__, 'error': str(ex)}))

    def on_disconnect(client, userdata, rc):
        logging.info("Disconnected with return code " + str(rc))


    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.loop_start()

    while True:

        time.sleep(TIMEOUT_SEC)
        robot.tick()

        x, y, r = robot.position()

        client.publish("robot/state", json.dumps(robot.state()))
        client.publish("robot/position", json.dumps({'x': x, 'y': y, 'r': r}))


