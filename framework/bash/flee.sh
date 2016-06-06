#!/bin/bash

REVERT_THRESHOLD=50
REVERT_SPEED=-40

function stop_motor {
	echo "stop" > /sys/class/tacho-motor/motor0/command
	echo "stop" > /sys/class/tacho-motor/motor1/command
}

function activate_motor {
	echo "run-direct" > /sys/class/tacho-motor/motor0/command
	echo "run-direct" > /sys/class/tacho-motor/motor1/command
}

function set_motor_speed {
	echo $1 > /sys/class/tacho-motor/motor0/duty_cycle_sp
	echo $1 > /sys/class/tacho-motor/motor1/duty_cycle_sp
}

function reset_sensor {
	echo "IR-PROX" > /sys/class/lego-sensor/sensor0/mode
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
done



