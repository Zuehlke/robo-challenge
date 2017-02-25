#!/usr/bin/env python3

WHITE = ((0, 0, 200), (60, 10, 255))
ORANGE = ((8, 150, 100), (15, 255, 255))
CAMERA = 1

WORLD_WIDTH = 1280
WORLD_HEIGHT = 960
RADIUS = 25

import cv2


class RobotPositioningSystem:
    def __enter__(self):
        self.camera = cv2.VideoCapture(CAMERA)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, WORLD_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, WORLD_HEIGHT)
        return self

    def __exit__(self, type, value, traceback):
        self.camera.release()

    def locate_robot_on_frame(self, color):
        grabbed, frame = self.camera.read()
        return RobotPositioningSystem.locate_robot(frame, color)

    @staticmethod
    def locate_robot(image, color):
        color_lower = color[0]
        color_upper = color[1]

        # blurred = cv2.GaussianBlur(image, (11, 11), 0)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, color_lower, color_upper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) == 0:
            return None
        c = max(cnts, key=cv2.contourArea)
        M = cv2.moments(c)

        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        return  center[0], WORLD_HEIGHT - center[1]


import paho.mqtt.client as mqtt
import json


class RoboRadio:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.client = mqtt.Client("Robo Positioning System")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        return self

    def __exit__(self, type, value, traceback):
        self.client.disconnect()

    def publish_location(self, location):
        payload = json.dumps({'x': location[0], 'y': location[1], 'r': RADIUS})
        self.client.publish("robot/position", payload)

    def process_messages(self):
        self.client.loop()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))


def main_loop():
    with RobotPositioningSystem() as rps:
        with RoboRadio("broker", 1883) as radio:
            while True:
                radio.process_messages()
                location = rps.locate_robot_on_frame(WHITE)

                if location is None:
                    continue

                radio.publish_location(location)

if __name__ == "__main__":
    main_loop()

