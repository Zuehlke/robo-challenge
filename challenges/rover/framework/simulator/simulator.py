# -*- coding: utf-8 -*-
import math
import common

class Simulator:
    """
    Simulator for the robot and positional system.
    """

    MAX_DIST = 5000
    MIN_DIST = 0
    MAX_ANGLE = 360
    MIN_ANGLE = 0

    # round x/y position
    ROUND_DIGITS = 0
    # The radius of the robot in cm
    RADIUS_CM = 7
    # factor robot distance (tacho counts) to cm (20 tacho counts ca. 1 cm)
    TACHO_COUNT_CM_FACTOR = 20
    # factor between robot distance and x/y positional system
    # WORLD DISTANCE = POSITION FACTOR * ROBOT DISTANCE
    POSITION_FACTOR = 3.328125

    def __init__(self, x=0, y=0, r=15, angle=0):
        """
        Initialize the robot simulator and positional system.
        :param x: the horizontal starting position.
        :param y: the vertical starting position.
        :param r: the radius
        :param angle: the starting angle in degrees.
        """
        self.__x = x
        self.__y = y
        self.__r = r
        self.__angle = angle

        self.__start_x = self.__x
        self.__start_y = self.__y
        self.__start_angle = self.__angle

        self.__left_distance = 0
        self.__right_distance = 0

    @common.check_int
    @common.max(MAX_DIST)
    @common.min(MIN_DIST)
    def forward(self, distance):
        """
        Move the robot forward by a given distance.
        :param distance: the distance the robot should move forward.
        :return: None
        """
        x = math.cos(math.radians(self.__angle)) * distance / self.POSITION_FACTOR
        y = math.sin(math.radians(self.__angle)) * distance / self.POSITION_FACTOR
        self.__x += x
        self.__y += y
        self.__left_distance += distance
        self.__right_distance += distance

    @common.check_int
    @common.max(MAX_DIST)
    @common.min(MIN_DIST)
    def backward(self, distance):
        """
        Move the robot backward by a given distance.
        :param distance: the distance the robot should move backward.
        :return: None
        """
        x = math.cos(math.radians(self.__angle)) * distance / self.POSITION_FACTOR
        y = math.sin(math.radians(self.__angle)) * distance / self.POSITION_FACTOR
        self.__x -= x
        self.__y -= y
        self.__left_distance -= distance
        self.__right_distance -= distance

    @common.check_int
    @common.max(MAX_ANGLE)
    @common.min(MIN_ANGLE)
    def right(self, angle):
        """
        Turn the robot right by a given angle (degrees).
        :param angle: the angle in degrees.
        :return: None
        """
        self.__angle -= angle
        distance = self.calc_distance_with_angle(angle)
        self.__right_distance -= distance
        self.__left_distance += distance

    @common.check_int
    @common.max(MAX_ANGLE)
    @common.min(MIN_ANGLE)
    def left(self, angle):
        """
        Turn the robot left by a given angle (degrees).
        :param angle: the angle in degrees.
        :return: None
        """
        self.__angle += angle
        distance = self.calc_distance_with_angle(angle)
        self.__right_distance += distance
        self.__left_distance -= distance

    def reset(self):
        """
        Sets the robot back to the staring position.
        :return: None
        """
        self.__x = self.__start_x
        self.__y = self.__start_y
        self.__angle = self.__start_angle
        self.__right_distance = 0
        self.__left_distance = 0

    def angle(self):
        """
        The current angle in degrees.
        :return: the angle degrees.
        """
        return self.__angle

    def position(self):
        """
        The current position adn radius (x,y,r) from the robot.
        :return: the x, y coordinates and radius as tuple
        """
        return int(round(self.__x, self.ROUND_DIGITS)), int(round(self.__y, self.ROUND_DIGITS)), self.__r

    def stop(self):
        """
        Stops the robot
        :return: None
        """
        pass

    def state(self):
        """
        Returns the state of the robot (distance right / left motor and angle)
        :return: map {'right_motor', 'lef_motor', 'angle'} with the current values distance
        left motor, distance right motor and current angle in degrees of the robot.

        The real angle from gyro is the current angle multiplied with -1

        """
        out = {
            'right_motor': self.__right_distance,
            'left_motor': self.__left_distance,
            'angle': self.angle() * -1
        }

        return out

    def calc_distance_with_angle(self, angle):
        """
        Calculate the distance when the robot turns a given angle in degree.
        :param angle: angle in degree
        :return: distance in tacho counts
        """
        return round(2 * self.RADIUS_CM * math.pi * angle / 360 * self.TACHO_COUNT_CM_FACTOR)

    def __str__(self):
        return "x: %s, y: %s, angle: %s" % (self.__x, self.__y, self.__angle)


class TimeDecorator:
    """
    Decorator for the Simulator, extends the Simulator with dimension time.
    """

    TACHO_COUNT_PER_TICK = 20

    def __init__(self, simulator):
        self.simulator = simulator
        self.next = {'command': None, 'value': 0}

    def __getattr__(self, name):
        return getattr(self.simulator, name)

    def forward(self, distance):
        self.next['command'] = 'forward'

        if distance <= self.TACHO_COUNT_PER_TICK:
            self.simulator.forward(distance)
            self.next['value'] = 0
        else:
            self.simulator.forward(self.TACHO_COUNT_PER_TICK)
            self.next['value'] = distance - self.TACHO_COUNT_PER_TICK

    def backward(self, distance):
        self.next['command'] = 'backward'

        if distance <= self.TACHO_COUNT_PER_TICK:
            self.simulator.backward(distance)
            self.next['value'] = 0
        else:
            self.simulator.backward(self.TACHO_COUNT_PER_TICK)
            self.next['value'] = distance - self.TACHO_COUNT_PER_TICK

    def reset(self):
        self.next = {'command': None, 'value': 0}
        self.simulator.reset()

    def stop(self):
        self.next = {'command': None, 'value': 0}

    def left(self, angle):
        self.simulator.left(angle)
        self.next = {'command': None, 'value': 0}

    def right(self, angle):
        self.simulator.right(angle)
        self.next = {'command': None, 'value': 0}

    def __str__(self):
        return str(self.simulator)

    def tick(self):

        command = self.next['command']

        if command == 'forward':
            rest = self.next['value']
            self.forward(rest)

        if command == 'backward':
            rest = self.next['value']
            self.backward(rest)


