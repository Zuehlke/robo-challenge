# -*- coding: utf-8 -*-
import random
import math

WORLD_WIDTH = 1280
WORLD_HEIGHT = 960


class Point:
    """
    A point in the game world. A point has a score which is
    earned when the point was collected by the robot.
    """

    def __init__(self, x, y, r):
        """
        A point with x, y coordinates and a radius r.
        :param x: the x coordinate
        :param y: the y coordinate
        :param r: the radius
        """
        self.x = x
        self.y = y
        self.r = r
        self.collected = False
        self.score = 1

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y) + ", r:" + str(self.r)


class Game:
    """
    The game engine -  master of the points and score
    """

    def __init__(self, radius=5, max_x=WORLD_WIDTH, max_y=WORLD_HEIGHT, distance=100, pointsCreator=None):

        self.__max_y = max_y
        self.__max_x = max_x
        self.__radius = radius

        x_center = round(max_x / 2)
        y_center = round(max_y / 2)
        self.__x_center = x_center
        self.__y_center = y_center
        self.__distance = distance

        self.__pointsCreator = pointsCreator or RandomPointsCreator(radius, distance)
        self.__points = pointsCreator.create_points(max_x, max_y)

    def reset(self):
        """
        Reset the game and world
        :return: None
        """
        self.__points = self.__pointsCreator.create_points(self.max_x(), self.max_y())


    def points(self):
        return self.__points

    def max_x(self):
        return self.__max_x

    def max_y(self):
        return self.__max_y

    def center_x(self):
        return self.__x_center

    def center_y(self):
        return self.__y_center

    def radius(self):
        return self.__radius

    def distance(self):
        return self.__distance

    def points(self):
        return self.__points

    def check(self, x, y, r):

        for p in self.__points:
            distance = r + p.r

            if math.pow(x - p.x, 2) + math.pow(y - p.y, 2) < math.pow(distance, 2):
                # robot has found the point
                p.collected = True

    def score(self):
        return sum([p.score for p in self.points() if p.collected])

    def __str__(self):
        return "points: %s, x: %s, y: %s, r: %s" % (
        len(self.__points), self.__max_x, self.__max_y, self.__radius)


class RandomPointsCreator:
    def __init__(self,radius, distance, n_points=50, ratio_anti_points=0.1):
        self.__radius = radius
        self.__distance = distance
        self.__n_points = n_points
        self.__ratio_anti_points = ratio_anti_points

    def create_coordinate(self, max_x, max_y):
        x = random.randint(self.__radius * 2, max_x - self.__radius * 2)
        y = random.randint(self.__radius * 2, max_y - self.__radius * 2)
        return x, y

    def create_points(self, max_x, max_y):
        x_center = round(max_x / 2)
        y_center = round(max_y / 2)

        points = []

        for i in range(self.__n_points):

            x, y = self.create_coordinate(max_x, max_y)

            while math.pow(x - round(x_center), 2) + math.pow(y - round(y_center), 2) < math.pow(self.__distance, 2):
                x, y = self.create_coordinate(max_x, max_y)

            points.append(Point(x=x, y=y, r=self.__radius))

        # create anti points
        n_anti_points = min(int(self.__n_points * self.__ratio_anti_points), len(points))

        for i in range(n_anti_points):
            points[i - len(points)].score = -1

        return points
