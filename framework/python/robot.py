#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ev3dev.ev3 as ev3

###
# SETUP
##

# motors
motor_right = ev3.LargeMotor('outA')
print("motorRight connected: %s" % str(motor_right.connected))

motor_left = ev3.LargeMotor('outB')
print("motorRight connected: %s" % str(motor_right.connected))

motors = [motor_left, motor_right]
motor_right.reset()
motor_left.reset()

# sensors
color_sensor = ev3.ColorSensor()
print("color sensor connected: %s" % str(color_sensor.connected))
color_sensor.mode = 'COL-REFLECT'

ultrasonic_sensor = ev3.UltrasonicSensor()
print("ultrasonic sensor connected: %s" % str(ultrasonic_sensor.connected))
ultrasonic_sensor.mode = 'US-DIST-CM'


# sleep timeout
sleep_timeout_sec = 0.1

# default duty_cycle (0 - 100)
default_duty_cycle = 60

# threshold distance
threshold_distance = 90


def backward():

    for m in motors:
        duty_cycle = m.duty_cycle_sp
        if duty_cycle > 0:
            m.duty_cycle_sp = duty_cycle * -1

    for m in motors:
        m.run_direct()


def forward():

    for m in motors:
        duty_cycle = m.duty_cycle_sp
        if duty_cycle < 0:
            m.duty_cycle_sp = duty_cycle * -1

    for m in motors:
        m.run_direct()


def set_speed(duty_cycle):
    for m in motors:
        m.duty_cycle_sp = duty_cycle


def brake():
    for m in motors:
        m.stop()


def turn():
    motor_left.stop()
    pos = motor_right.position

    # new absolute position
    abs_pos = pos + 500

    motor_right.position_sp = abs_pos
    motor_right.run_to_abs_pos()

    while abs(motor_right.position - abs_pos) > 10:
        # turn

        # stop when object detected
        if ultrasonic_sensor.value() < threshold_distance:
            break

    set_speed(default_duty_cycle)
    forward()


def teardown():
    print('teardown')
    for m in motors:
        m.stop()
        m.reset()


def run():
    print('run robot, run!')

    set_speed(default_duty_cycle)
    forward()

    try:
        # game loop (endless loop)
        while True:
            time.sleep(sleep_timeout_sec)
            print('color value: %s' % str(color_sensor.value()))
            print('ultrasonic value: %s' % str(ultrasonic_sensor.value()))

            # found obstacle
            if ultrasonic_sensor.value() < threshold_distance:

                brake()

                # drive backwards for 0.5 sec
                backward()
                time.sleep(0.5)

                # turn
                turn()

            else:
                forward()

    # hanlde ctr+c and system exit
    except (KeyboardInterrupt, SystemExit):
        teardown()
        raise

    except Exception as e:
        print('ohhhh error!')
        print(e)
        teardown()

# run robot
run()
