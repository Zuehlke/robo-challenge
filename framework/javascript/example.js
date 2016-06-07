#!/usr/bin/env node

var ev3dev = require('ev3dev-lang');

//var motor0 = "/sys/class/tacho-motor/motor0/";
//var motor1 = "/sys/class/tacho-motor/motor1/";
var INITIAL_SPEED = 30;
var INITIAL_CYCLE = 50;
var DISTANCE_THRESHOLD = 300;
var LOOP_INTERVAL = 200;

var ultrasonic; //= "/sys/class/lego-sensor/sensor0/";
var motorRight;
var motorLeft;

function setUp() {
  console.log("Setting up...");

  motorRight = new ev3dev.LargeMotor(ev3dev.OUTPUT_C);
  console.log("motorRight connected: " + motorRight.connected);
  motorLeft = new ev3dev.LargeMotor(ev3dev.OUTPUT_B);
  console.log("motorLeft connected: " + motorLeft.connected);

  ultrasonic = new ev3dev.UltrasonicSensor(ev3dev.INPUT_3);
  console.log("ultrasonic connected: " + ultrasonic.connected);

  motorRight.reset();
  motorLeft.reset();

  motorRight.speedSp = INITIAL_SPEED;
  motorLeft.speedSp = INITIAL_SPEED;

  motorRight.dutyCycleSp = INITIAL_CYCLE;
  motorLeft.dutyCycleSp = INITIAL_CYCLE;
}

function tearDown() {
  console.log("Tearing down...");

  motorRight.stop();
  motorLeft.stop();
}

function main() {
  console.log("Nodejs started.");

  setUp();

  setInterval(function() {
    run_loop();
  }, LOOP_INTERVAL);
}

function run_loop() {
  if (!motorRight.isRunning && !motorLeft.isRunning) {
    motorRight.runForever(INITIAL_SPEED);
    motorLeft.runForever(INITIAL_SPEED);
  }

  if (check_obstacle()) {
    console.log("Found obstacle!");
    turn(90);
  }

}

function check_obstacle() {
  var distance = ultrasonic.getValue(0);
  return distance < DISTANCE_THRESHOLD;
}

function turn(steps) {
  console.log("Turning " + steps + " steps");
  motorRight.runToRelativePosition(steps, INITIAL_SPEED);
  motorLeft.runToRelativePosition(-steps, INITIAL_SPEED);
}

// handling exits

process.stdin.resume();//so the program will not close instantly

function exitHandler(options, err) {
    if (options.cleanup) tearDown();
    if (err) console.log(err.stack);
    if (options.exit) process.exit();
}

//do something when app is closing
process.on('exit', exitHandler.bind(null,{cleanup:true}));

//catches ctrl+c event
process.on('SIGINT', exitHandler.bind(null, {exit:true}));

//catches uncaught exceptions
process.on('uncaughtException', exitHandler.bind(null, {exit:true}));


// start the program
main();
