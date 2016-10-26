#!/bin/bash

REVERT_THRESHOLD=100
REVERT_SPEED=-400

function stop_motor {
	echo "stop" > /sys/class/tacho-motor/motor0/command
	echo "stop" > /sys/class/tacho-motor/motor1/command
}

function activate_motor {
	echo "run-forever" > /sys/class/tacho-motor/motor0/command
	echo "run-forever" > /sys/class/tacho-motor/motor1/command
}

function set_motor_speed {
	echo $1 > /sys/class/tacho-motor/motor0/speed_sp
	echo $1 > /sys/class/tacho-motor/motor1/speed_sp
}

function reset_sensor {
	echo "US-DIST-CM" > /sys/class/lego-sensor/sensor0/mode
}

function reset_motor {
	stop_motor
	activate_motor	
}

function read_prox {
	cat /sys/class/lego-sensor/sensor0/value0
}

function determine_motor_speed {
	if [ "$1" -lt "${REVERT_THRESHOLD}" ]
	then
		echo ${REVERT_SPEED}
	else
		echo 0
	fi	
}

function cleanup {
	echo "Cleaning up..."
	stop_motor
}
trap cleanup EXIT

reset_motor
reset_sensor
activate_motor
while [ true ]
do 
	prox=$(read_prox)
	speed=$(determine_motor_speed $prox)
	echo -e "PROX:\t${prox}\tSPEED:\t${speed}"
	set_motor_speed $speed
    activate_motor
done



