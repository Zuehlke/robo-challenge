// Create a client instance
var client = new Paho.MQTT.Client(location.hostname, Number(9001), guid());

var doUpdate = true;
var zoomFactor = 0.5;

var viewState = { leaderboard: [], currentGame: {} ,
    currentScore: {}, robotState: {}, robotPosition: {},
    currentWorld: {}, control: { angle: 90, distance: 100, zoomFactor: zoomFactor}};

// do reconnect when connection is lost
setInterval(function(){
    reconnectIfConnectionIsLost(client);
}, 3000);


function guid() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
        s4() + '-' + s4() + s4() + s4();
}


function reconnectIfConnectionIsLost(client) {
    if(!client.isConnected()) {
        console.log("try to reconnect");
        client.connect({onSuccess:onConnect});
    }
}

function zoom(value) {
    document.body.style.zoom = value;
}


// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription.
    console.log("onConnect");
    client.subscribe("robot/state");
    client.subscribe("game/state");
    client.subscribe("tournament");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:"+responseObject.errorMessage);
    }
}


function drawRobot(robot, world, factor) {
    var c = $("#robot_layer");
    var ctx = c[0].getContext('2d');

    var x_max = world.x_max * factor;
    var y_max = world.y_max * factor;
    var x = robot.x * factor;
    var y = robot.y * factor;
    var r = robot.r * factor;

    ctx.canvas.height = y_max;
    ctx.canvas.width = x_max;

    ctx.translate(0, y_max);
    ctx.scale(1, -1);

    ctx.clearRect(0, 0, x_max, y_max);

    ctx.beginPath();
    ctx.lineWidth = 1;

    ctx.arc(x, y, r, 2 * Math.PI, false);
    ctx.fillStyle = "#c12676";
    ctx.strokeStyle = "#8a0035";
    ctx.fill();
    ctx.stroke();

}

function getScore(points){
    var total = 0;
    var current = 0;
    for (var i = 0; i < points.length; i++) {
        total += points[i].score;
        if(points[i].collected) {
            current += points[i].score;
        }
    }
    return {'max': total, 'current': current};
}

function drawPoints(ctx, points, factor) {
    $.each(points, function(index, point) {

        var x = point.x * factor;
        var y = point.y * factor;
        var r =  point.r * factor;

        ctx.beginPath();
        ctx.lineWidth = 1;
        ctx.fillStyle = "#12c122";
        ctx.strokeStyle = "#12c122";
        ctx.arc(x, y, r, 2 * Math.PI, false);

        if (point.collected) {
            ctx.fillStyle = "#ffeef6";
            ctx.strokeStyle = "#c3c3c3";
        }
        ctx.fill();
        ctx.stroke();
    });
}

function drawWorld(ctx, world, factor) {

    var y_max = world.y_max * factor;
    var x_max = world.x_max * factor;

    ctx.canvas.height = y_max;
    ctx.canvas.width = x_max;

    ctx.lineWidth = 1;

    ctx.clearRect(0, 0, x_max , y_max);

    ctx.translate(0, y_max);
    ctx.scale(1, -1);

    function getMousePos(canvas, evt) {

        var rect = canvas.getBoundingClientRect();


        return {
            x: Math.round(evt.clientX - rect.left),
            y: Math.round(Math.abs(evt.clientY - rect.top - canvas.height))
        };
    }

    ctx.canvas.addEventListener('mousemove', function(evt) {
        //viewState.notice['mouse'] = getMousePos(ctx.canvas, evt);
    }, false);



    //viewState.notice['world'] = body.world;

    doUpdate = false;
}

// called when a message arrives
function onMessageArrived(message) {

    var c = $("#map_layer");
    var ctx = c[0].getContext('2d');

    var body = JSON.parse(message.payloadString);
    if (message.destinationName === 'game/state') {

        var robot = body.robot;
        var world = body.world;
        var points = body.points;

        if(doUpdate) {
            // redraw world
            drawWorld(ctx, world, zoomFactor);
        } else {

            drawPoints(ctx, points, zoomFactor);
            drawRobot(robot, world,  zoomFactor);

            viewState.robotPosition = robot;
            viewState.currentWorld = world;
            viewState.currentScore = getScore(points);

        }
    }

    if (message.destinationName === 'robot/state') {
        viewState.robotState = body;
    }

    if(message.destinationName === 'tournament') {
        viewState.leaderboard = body.leaderboard;
        viewState.currentGame = body.currentGame;
    }

}

var currentGame = new Vue({
    el: '#currentGame',
    data: viewState
});

var leaderboard = new Vue({
    el: '#leaderboard',
    data: viewState,
    methods: {
        prepareGame: function(player) {
            var message = new Paho.MQTT.Message(JSON.stringify({
                "command": "prepare",
                "args": [player]
            }));

            message.destinationName = "gamemaster";
            client.send(message);

            message = new Paho.MQTT.Message(JSON.stringify({
                "command": "reset"}
            ));

            message.destinationName = "robot/process";
            client.send(message);

            doUpdate = true;
        }
    }
});

var control = new Vue({
    el: '#control',
    data: viewState,
    methods: {
        forward: function(distance) {
            var message = new Paho.MQTT.Message(JSON.stringify({
                "command": "forward",
                "args": [parseInt(distance)]
            }));

            message.destinationName = "robot/process";
            client.send(message);
        },
        backward: function(distance) {
            var message = new Paho.MQTT.Message(JSON.stringify({
                "command": "backward",
                "args": [parseInt(distance)]
            }));

            message.destinationName = "robot/process";
            client.send(message);
        },
        left: function(angle) {
            var message = new Paho.MQTT.Message(JSON.stringify({
                "command": "left",
                "args": [parseInt(angle)]
            }));

            message.destinationName = "robot/process";
            client.send(message);
        },
        right: function(angle) {
            var message = new Paho.MQTT.Message(JSON.stringify({
                "command": "right",
                "args": [parseInt(angle)]
            }));

            message.destinationName = "robot/process";
            client.send(message);
        },
        reset: function() {
            var message = new Paho.MQTT.Message(JSON.stringify({
                "command": "reset"}
            ));

            message.destinationName = "robot/process";
            client.send(message);
        },
        stop: function() {
            var message = new Paho.MQTT.Message(JSON.stringify({
                "command": "stop"
            }));

            message.destinationName = "robot/process";
            client.send(message);
        }
    }
});

var notice = new Vue({
    el: '#notice',
    data: viewState
});

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});