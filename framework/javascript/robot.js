#!/usr/bin/env node

var ev3dev = require('ev3dev-lang');

var DEFAULT_SLEEP_TIMEOUT_IN_MSEC = 100;

// default duty_cycle (0 - 100)
var DEFAULT_DUTY_CYCLE = 60;
var DEFAULT_THRESHOLD_DISTANCE = 90;

//
// Setup
//
console.log("Setting up...");

// motors
var motorRight = new ev3dev.LargeMotor(ev3dev.OUTPUT_A);
console.log("motorRight connected: " + motorRight.connected);
var motorLeft = new ev3dev.LargeMotor(ev3dev.OUTPUT_B);
console.log("motorLeft connected: " + motorLeft.connected);

var motors = [motorLeft, motorRight];

motorRight.reset();
motorLeft.reset();


// sensors
var colorSensor = new ev3dev.ColorSensor(ev3dev.INPUT_AUTO);
console.log("color sensor connected: " + colorSensor.connected);
colorSensor.mode = "COL-REFLECT";


var ultrasonicSensor = new ev3dev.UltrasonicSensor(ev3dev.INPUT_AUTO);
console.log("ultrasonic connected: " + ultrasonicSensor.connected);
ultrasonicSensor.mode = "US-DIST-CM";


//
// Robot functionality
//
function backward() {
    for (var i = 0; i < motors.length; i++) {
        var currentDutyCycle = motors[i].dutyCycleSp;

        if (currentDutyCycle > 0) {
            motors[i].dutyCycleSp = currentDutyCycle * -1;
        }
        motors[i].runForever();
    }
}

function forward() {
    for (var i = 0; i < motors.length; i++) {
        var currentDutyCycle = motors[i].dutyCycleSp;

        if (currentDutyCycle < 0) {
            motors[i].dutyCycleSp = currentDutyCycle * -1;
        }
        motors[i].runForever();
    }
}

function setSpeed(dutyCycle) {
    for (var i = 0; i < motors.length; i++) {
        motors[i].dutyCycleSp = dutyCycle;
    }
}

function brake() {
    for (var i = 0; i < motors.length; i++) {
        motors[i].stop();
    }
}

function turn() {
    motorLeft.stop();
    var pos = motorRight.position;

    // new absolute position
    var absPos = pos + 500;
    motorRight.runToAbsolutePosition(absPos);

    while (Math.abs(motorRight.position - absPos) > 10) {
        // turn to new position

        // stop when object detected
        if(ultrasonicSensor.getValue(0) < DEFAULT_THRESHOLD_DISTANCE) {
            break;
        }
    }

    setSpeed(DEFAULT_DUTY_CYCLE);
    forward();

}


function tearDown() {
    console.log("Tearing down...");

    for (var i = 0; i < motors.length; i++) {
        motors[i].stop();
        motors[i].reset();
    }
}

function main() {
    console.log("Run robot, run!");

    setSpeed(DEFAULT_DUTY_CYCLE);
    forward();

    // game loop (endless loop)
    setInterval(function () {
        run_loop();
    }, DEFAULT_SLEEP_TIMEOUT_IN_MSEC);
}

function run_loop() {

    console.log("color value: " + colorSensor.getValue(0))
    console.log("ultrasonic value: " + ultrasonicSensor.getValue(0))
    console.log("motor positions (r, l): " + motorRight.position + ", "  + motorLeft.position)

    // found obstacle
    if (ultrasonicSensor.getValue(0) < DEFAULT_THRESHOLD_DISTANCE) {

        setSpeed(35);
        brake();

        // drive backwards
        backward();

        var newPos = motorRight.position - 200;
        var timeout = new Date();
        while (motorRight.position - newPos > 10) {
            // wait until robot has reached the new position or timeout (milliseconds) has expired
            if(new Date().getTime() - timeout.getTime() > 5000) break;
        }

        // turn
        turn();


    } else {
        forward();
    }

}


// doing a cleanup action just before node.js exits,
// see http://stackoverflow.com/questions/14031763/doing-a-cleanup-action-just-before-node-js-exits

// handling exits
process.stdin.resume();//so the program will not close instantly

function exitHandler(options, err) {
    if (options.cleanup) tearDown();
    if (err) console.log(err.stack);
    if (options.exit) process.exit();
}

// do something when app is closing
process.on('exit', exitHandler.bind(null, {cleanup: true}));

// catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {exit: true}));

// catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, {exit: true}));

//
// start the program
//
main();
