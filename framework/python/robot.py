#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import ev3dev.ev3 as ev3

# default sleep timeout in sec
DEFAULT_SLEEP_TIMEOUT_IN_SEC = 0.1

# default speed
DEFAULT_SPEED = 600

# default threshold distance
DEFAULT_THRESHOLD_DISTANCE = 90

##
# Setup
##

print("Setting up...")

# motors
right_motor = ev3.LargeMotor('outA')
print("motor right connected: %s" % str(right_motor.connected))

left_motor = ev3.LargeMotor('outB')
print("motor left connected: %s" % str(right_motor.connected))

motors = [left_motor, right_motor]
right_motor.reset()
left_motor.reset()

# sensors
color_sensor = ev3.ColorSensor()
print("color sensor connected: %s" % str(color_sensor.connected))
color_sensor.mode = 'COL-REFLECT'

ultrasonic_sensor = ev3.UltrasonicSensor()
print("ultrasonic sensor connected: %s" % str(ultrasonic_sensor.connected))
ultrasonic_sensor.mode = 'US-DIST-CM'


##
#  Robot functionality
##
def backward():

    for m in motors:
        speed = m.speed_sp
        if speed > 0:
            m.speed_sp = speed * -1

        m.run_forever()


def forward():

    for m in motors:
        speed = m.speed_sp
        if speed < 0:
            m.speed_sp = speed * -1

        m.run_forever()


def set_speed(speed):
    for m in motors:
        m.speed_sp = speed


def brake():
    for m in motors:
        m.stop()


def turn():
    left_motor.stop()
    pos = right_motor.position

    # new absolute position
    abs_pos = pos + 500

    right_motor.position_sp = abs_pos
    right_motor.run_to_abs_pos()

    while abs(right_motor.position - abs_pos) > 10:
        # turn to new position

        # stop when object detected
        if ultrasonic_sensor.value() < DEFAULT_THRESHOLD_DISTANCE:
            break

    set_speed(DEFAULT_SPEED)
    forward()


def teardown():
    print('Tearing down...')
    for m in motors:
        m.stop()
        m.reset()


def run_loop():
    # game loop (endless loop)
    while True:
        time.sleep(DEFAULT_SLEEP_TIMEOUT_IN_SEC)
        print('color value: %s' % str(color_sensor.value()))
        print('ultrasonic value: %s' % str(ultrasonic_sensor.value()))
        print('motor positions (r, l): %s, %s' % (str(right_motor.position), str(left_motor.position)))

        # found obstacle
        if ultrasonic_sensor.value() < DEFAULT_THRESHOLD_DISTANCE:

            set_speed(DEFAULT_SPEED / 2)
            brake()

            # drive backwards
            backward()

            new_pos = right_motor.position - 200
            timeout = time.time()

            while right_motor.position - new_pos > 10:
                # wait until robot has reached the new position or timeout (seconds) has expired
                if time.time() - timeout > 5:
                    break

            # turn
            turn()

        else:
            forward()


def main():
    print('Run robot, run!')

    set_speed(DEFAULT_SPEED)
    forward()

    try:
        run_loop()

    # doing a cleanup action just before program ends
    # handle ctr+c and system exit
    except (KeyboardInterrupt, SystemExit):
        teardown()
        raise

    # handle exceptions
    except Exception as e:
        print('ohhhh error!')
        print(e)
        teardown()
##
# start the program
##
main()
