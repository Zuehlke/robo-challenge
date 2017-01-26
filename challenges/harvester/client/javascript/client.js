#!/usr/bin/env node
var mqtt = require('mqtt')

var SERVER = "127.0.0.1";
var PORT = 1883;


var client  = mqtt.connect({host: SERVER, port: PORT});

client.on('connect', function () {
    client.subscribe('robot/state');
    client.subscribe('game/position');
});

client.on('message', function (topic, message) {
    // message is Buffer
    console.log(topic);
    console.log(message.toString());

    // TODO: implement algorithm

});


function tearDown() {
    console.log("Tearing down...");
    client.end();
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
