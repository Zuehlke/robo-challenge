# -*- coding: utf-8 -*-

import unittest
import turtle
import simulator as api


class BasicTestSuite(unittest.TestCase):

    def setUp(self):
        t = turtle.Turtle()
        t.speed(0)
        self.__turtle = t

    def compare_pos(self, pos1, pos2, factor=3.328125):
        self.assertAlmostEqual(pos1[0], round(pos2[0] / factor, 0), delta=0.01)
        self.assertAlmostEqual(pos1[1], round(pos2[1] / factor, 0), delta=0.01)

    def test_init_default(self):
        sim = api.Simulator()
        self.assertEqual(sim.angle(), 0)
        self.assertEqual(sim.position(), (0, 0, 15))

    def test_init_with_values(self):
        x = 10
        y = 20
        angle = 90
        r = 15

        sim = api.Simulator(x=x, y=y, angle=angle, r=r)
        self.assertEqual(sim.angle(), angle)
        self.assertEqual(sim.position(), (x, y, r))

    def test_forward(self):
        sim = api.Simulator()
        distance = 100
        self.__turtle.forward(distance)
        sim.forward(distance)
        self.compare_pos(sim.position(), self.__turtle.position())

    def test_backward(self):
        sim = api.Simulator()
        distance = 180
        self.__turtle.backward(distance)
        sim.backward(distance)
        self.compare_pos(sim.position(), self.__turtle.position())

    def test_right(self):
        sim = api.Simulator()
        distance = 90
        angle = 45
        self.__turtle.right(angle)
        self.__turtle.forward(distance)

        sim.right(angle)
        sim.forward(distance)

        self.compare_pos(sim.position(), self.__turtle.position())

    def test_left(self):
        sim = api.Simulator()
        distance = 180
        angle = 70
        self.__turtle.left(angle)
        self.__turtle.forward(distance)

        sim.left(angle)
        sim.forward(distance)

        self.compare_pos(sim.position(), self.__turtle.position())

    def test_multiple_moves(self):
        sim = api.Simulator()
        distance = 180
        angle = 70
        self.__turtle.left(angle)
        self.__turtle.forward(distance)
        self.__turtle.backward(distance/2)
        self.__turtle.right(angle * 2)

        sim.left(angle)
        sim.forward(distance)
        sim.backward(int(distance/2))
        sim.right(angle * 2)

        self.compare_pos(sim.position(), self.__turtle.position())

        self.__turtle.backward(distance * 3)
        sim.backward(distance * 3)

        self.compare_pos(sim.position(), self.__turtle.position())

        self.__turtle.right(340)
        self.__turtle.forward(distance)

        sim.right(340)
        sim.forward(distance)

        self.compare_pos(sim.position(), self.__turtle.position())

    def test_distance_simple(self):
        sim = api.Simulator()
        distance = 180

        sim.forward(distance)
        self.assertEqual(sim.state(), {'angle': 0, 'left_motor': distance, 'right_motor': distance})

        sim.backward(distance)
        self.assertEqual(sim.state(), {'angle': 0, 'left_motor': 0, 'right_motor': 0})

    def test_distance_right(self):
        sim = api.Simulator()

        sim.right(90)
        self.assertEqual(sim.state(), {'angle': 90, 'left_motor': 220, 'right_motor': -220})

    def test_distance_left(self):
        sim = api.Simulator()

        sim.left(90)
        self.assertEqual(sim.state(), {'angle': -90, 'left_motor': -220, 'right_motor': 220})


