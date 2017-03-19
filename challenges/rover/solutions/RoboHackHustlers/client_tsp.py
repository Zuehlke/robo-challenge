import paho.mqtt.client as mqtt
import json
import math
# from game_logic import Logic
import time
import random

from tsp_solver.greedy import solve_tsp

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def dist(a, b):
        return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)

    def to_dict(self):
        return dict(x=self.x, y=self.y)
    @staticmethod
    def get_angle(a,b):
        d_rot = math.atan2(b.y - a.y, b.x - a.x)
        d_rot_deg = math.degrees(d_rot) % 360
        if d_rot_deg > 180:
            d_rot_deg = -360 + d_rot_deg
        return d_rot_deg



class Logic:
    def __init__(self, max_stat_count=5, min_angle_err=10, stat_err=0, fact_step=5, calibration=False):
        self.available = list()                      # List of all unotuched pos pts
        self.max_stat_count = max_stat_count         # if after max_stat_count the position did nto change, im stationary.
        self.stat_count = max_stat_count             # current_counter for finding stationary
        self.robot = None                            # Point of current position of robot.
        self.rob_angle = 0                           # Absolute orientation of robot in radians.

        self.stat_err = stat_err                     # tolerance for stationary, if its below this you increment stat_count.
        self.min_angle_err = min_angle_err
        self.angle_err = 180                           # if difference target rotation and current rotation is (-eps, eps) then dont turn.
        self.target = None                           # Point as the target where robot wants to move.
        self.target_dist = 0
        self.count_target_update = 0
        self.max_count_target_update = 3
        self.factor_step = fact_step                 # figure it out with initial calibration. If you have a target dist d you multiply it by this factor to make up for the noise in the real robot.
        self.x_max = 0
        self.y_max = 0
        self.direction = "forward"
        self.tsp_created = False
        self.tsp_path = None
        self.tsp_index = 0

    def update(self, data):
        robo = Point(data['robot']['x'], data['robot']['y'])
        ava = [Point(p['x'], p['y']) for p in data['points'] if p['collected'] is False and p['score'] > 0]
        if not self.tsp_created:
            ava = [Point(p['x'], p['y']) for p in data['points'] if p['collected'] is False and p['score'] > 0]
            D = [[0 for i in range(len(ava))] for j in range(len(ava))]

            # connection between start point and all the ava points is 0 for tsp.

            # now add distances between the ava points.
            for i in range(len(ava)):
                for j in range(i + 1, len(ava)):
                    d = Point.dist(ava[i], ava[j])
                    D[i][j] = D[j][i] = d
            self.tsp_path = solve_tsp(D)
            for i in range(len(self.tsp_path)):
                self.tsp_path[i] = ava[self.tsp_path[i]]


        prev_angle = self.rob_angle

        if self.robot: #if its not the first update.
            stat = self.stationary(robo)
            self.rob_angle = math.atan2(robo.y - self.robot.y, robo.x - self.robot.x)
        else:
            stat = True
            self.available = ava
            self.x_max = data['world']['x_max']-4
            self.y_max = data['world']['y_max']-4

        self.robot = robo

        if stat:
            self.stat_count += 1
        else:
            self.stat_count = 0

        to_move = False
        found = False
        if len(ava) < len(self.available):
            print("**found")
            to_move = True
            found = True
        elif self.stat_count >= self.max_stat_count and abs(math.degrees(self.rob_angle-prev_angle)) <= self.min_angle_err:
            print("**stationary")
            to_move = True
        elif self.on_border():
            print("**border")
            to_move = True
        elif (self.count_target_update >= self.max_count_target_update
                    and Point.dist(self.robot, self.target) > self.target_dist) :
            print("**away from target")
            to_move = True
        else:

            if abs(Point.get_angle(self.robot, self.target)) > self.angle_err:
                print("**angle adjust")
                to_move = True

        if to_move:
            self.available = ava
            if not self.tsp_created:
                p = self.find_closest()
                self.tsp_created = True
            else:
                p = self.tsp_path[self.tsp_index]
                if found:
                    self.tsp_index += 1
            # stop()
            # TODO: move a little to find your orientation
            self.move(p)
        elif self.count_target_update >= self.max_count_target_update:
            self.count_target_update = 0
            self.target_dist = Point.dist(self.robot, self.target)
            self.angle_err = 0.33 * self.angle_err + self.min_angle_err


    def stationary(self, p):
        if abs(p.x-self.robot.x) > self.stat_err or abs(p.y-self.robot.y) > self.stat_err:
            return False
        else:
            return True

    def move(self, p):
        print("MOVE")
        print("robot", self.robot.x, self.robot.y)
        print("target", p.x, p.y)
        self.angle_err  = 180
        self.target = p
        self.count_target_update = 0
        d_trans = Point.dist(self.robot, p)
        self.target_dist = d_trans
        d_rot = math.atan2(p.y - self.robot.y, p.x - self.robot.x) - self.rob_angle
        d_rot_deg = math.degrees(d_rot) % 360
        if d_rot_deg > 180:
            d_rot_deg = -360+d_rot_deg
        print ("initial angle ", d_rot_deg)
        if abs(d_rot_deg) > 90:
            flip = True
        else:
            flip = False

        if flip:
            if self.direction == "forward":
                self.direction = "backward"
            else:
                self.direction = "forward"
            if d_rot_deg < 0:
                d_rot_deg += 180
            else:
                d_rot_deg -= 180


        turn(int(d_rot_deg), 2)
        if self.direction == "backward":
            move_backward(int(d_trans*self.factor_step))
        else:
            move_forward(int(d_trans*self.factor_step))

    def on_border(self):
        return self.robot.x > self.x_max or self.robot.y > self.y_max or self.robot.x < 4 or self.robot.y < 4


    def find_closest(self):
        mind = 2**31
        minp = None
        for p in self.available:
            d = Point.dist(self.robot, p)
            # print ("distance = ", d)
            if d < mind:
                mind = d
                minp = p
        return minp




SERVER = "127.0.0.1"
# SERVER = "10.10.10.30"
PORT = 1883
PLAYER_NAME = "RoboHackHustlers"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('players/' + PLAYER_NAME + '/#')
    client.subscribe('robot/state')
    client.publish('players/' + PLAYER_NAME, json.dumps({"command": "register"}))
    client.subscribe('players/' + PLAYER_NAME + '/incoming')

cur = dict()
cur['theta'] = 0
moving = False

logic = Logic(2, fact_step=4, min_angle_err=3)
first = True
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global cur, moving, logic, first
    obj = json.loads(msg.payload.decode("utf-8"))

    if 'incoming' in msg.topic:
        print(obj)
        client.publish('players/' + PLAYER_NAME, json.dumps({"command": "start"}))
        logic.rob_angle=0
    elif 'game' in msg.topic and not moving:
        if 'robot' in obj:
            # if first:
            #     move_forward(100)
            #     # time.sleep(2)
            #     first = False
            logic.update(obj)



def move_forward(dist):
    print("     forward ", dist)
    client.publish('robot/process', json.dumps({"command": "forward", "args": dist}))

def move_backward(dist):
    print("     back ", dist)
    client.publish('robot/process', json.dumps({"command": "backward", "args": dist}))

def turn(angle, err=0):
    print("     turn ", angle)
    if angle < -err:
        client.publish('robot/process', json.dumps({"command": "right", "args": -angle}))
    elif angle > err:
        client.publish('robot/process', json.dumps({"command": "left", "args": angle }))

def stop():
    print("     stop")
    client.publish('robot/process', json.dumps({"command": "stop"}))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(SERVER, PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:
    client.loop_forever()
except (KeyboardInterrupt, SystemExit):
    print("Tearing down...")
    client.disconnect()
    raise
