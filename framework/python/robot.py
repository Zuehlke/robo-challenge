#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ev3dev.ev3 as ev3

###
# GLOBAL VALUES
##

# motors
motor_right = ev3.LargeMotor('outA')
motor_left = ev3.LargeMotor('outB')

motors = [motor_left, motor_right]

# sensors
color_sensor = ev3.ColorSensor()
color_sensor.mode = 'COL-REFLECT'
ultrasonic_sensor = ev3.UltrasonicSensor()
ultrasonic_sensor.mode = 'US-DIST-CM'

# sleep timeout
sleep_timeout_sec = 0.1

# default speed (0 - 100)
normal_speed = 60


def backward():

    for m in motors:
        speed = m.duty_cycle_sp

        if speed > 0:
            m.duty_cycle_sp = speed * -1

    for m in motors:
        m.run_direct()


def forward():

    for m in motors:
        speed = m.duty_cycle_sp

        if speed < 0:
            m.duty_cycle_sp = speed * -1

    for m in motors:
        m.run_direct()


def set_speed(current_speed):
    for m in motors:
        m.duty_cycle_sp = current_speed


def brake():
    for m in motors:
        m.stop()



def turn():
    motor_left.stop()
    time.sleep(1)
    motor_left.run_direct()


def run():
    print('run robot, run!')

    set_speed(normal_speed)
    forward()

    # game loop
    while True:
        time.sleep(sleep_timeout_sec)
        print('color value: %s' % str(color_sensor.value()))
        print('ultrasonic value: %s' % str(ultrasonic_sensor.value()))

        if ultrasonic_sensor.value() < 70:

            brake()
            backward()
            time.sleep(0.5)
            turn()

        else:
            forward()

# run robot
run()
