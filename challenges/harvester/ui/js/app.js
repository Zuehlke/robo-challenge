// Create a client instance
var client = new Paho.MQTT.Client(location.hostname, Number(9001), "clientId");
var doUpdate = true;

var max_x = 0;
var max_y = 0;


$(document).ready(function() {
    $('#forward').click(function() {
        var message = new Paho.MQTT.Message(JSON.stringify({"command": "forward", "args": [parseInt($('#distance').val())]}));
        message.destinationName = "robot/process";
        client.send(message);
    });
});

$(document).ready(function() {
    $('#backward').click(function() {
        var message = new Paho.MQTT.Message(JSON.stringify({"command": "backward", "args": [parseInt($('#distance').val())]}));
        message.destinationName = "robot/process";
        client.send(message);
    });
});

$(document).ready(function() {
    $('#left').click(function() {
        var message = new Paho.MQTT.Message(JSON.stringify({"command": "left", "args": [parseInt($('#angle').val())]}));
        message.destinationName = "robot/process";
        client.send(message);
    });
});

$(document).ready(function() {
    $('#right').click(function() {
        var message = new Paho.MQTT.Message(JSON.stringify({"command": "right", "args": [parseInt($('#angle').val())]}));
        message.destinationName = "robot/process";
        client.send(message);
    });
});

$(document).ready(function() {
    $('#reset').click(function() {
        var message = new Paho.MQTT.Message(JSON.stringify({"command": "reset"}));
        message.destinationName = "game/process";
        client.send(message);

        message.destinationName = "robot/process";
        client.send(message);

        doUpdate = true;
    });
});

$(document).ready(function() {
    $('#stop').click(function() {
        var message = new Paho.MQTT.Message(JSON.stringify({"command": "stop"}));

        message.destinationName = "robot/process";
        client.send(message);
    });
});


function zoom(value) {
    console.log(value);
    document.body.style.zoom = value;
}


// called when the client connects
function onConnect() {
  // Once a connection has been made, make a subscription.
  console.log("onConnect");
  client.subscribe("robot/state");
  client.subscribe("game/position");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
  if (responseObject.errorCode !== 0) {
    console.log("onConnectionLost:"+responseObject.errorMessage);
  }
}


function drawRobot(x, y, r, max_x, max_y) {
    var c = $("#robot_layer");
    var ctx = c[0].getContext('2d');


    ctx.canvas.height = max_y;
    ctx.canvas.width = max_x;

    ctx.translate(0, max_y);
    ctx.scale(1, -1);

    ctx.clearRect(0, 0, max_x, max_y);

    ctx.beginPath();

    ctx.arc(x, y, r, 2 * Math.PI, false);
    ctx.fillStyle = "#c12676";
    ctx.fill();
    ctx.stroke();

}

function getScore(points){
    var total = 0;
    var current = 0
    for (var i = 0; i < points.length; i++) {
        total += points[i].score;
        if(points[i].collected) {
            current += points[i].score;
        }
    }
    return {'max': total, 'current': current};
}

function updatePoints(ctx, points) {
    $.each(points, function(index, point) {
        ctx.beginPath();
        ctx.arc(point.x, point.y, point.r, 0, 2 * Math.PI, false);

        if (point.collected) {
            ctx.fillStyle = "#6726c1";
            ctx.fill();
        }

        ctx.stroke();
    });
}

function createWorld(ctx, body) {
    ctx.canvas.height = body.world.y_max;
    ctx.canvas.width = body.world.x_max;

    ctx.clearRect(0, 0, max_x, max_y);

    max_x = body.world.x_max;
    max_y = body.world.y_max;

    ctx.translate(0, max_y);
    ctx.scale(1, -1);

    function getMousePos(canvas, evt) {

        var rect = canvas.getBoundingClientRect();


        return {
            x: Math.round(evt.clientX - rect.left),
            y: Math.round(Math.abs(evt.clientY - rect.top - canvas.height))
           };
     }

    ctx.canvas.addEventListener('mousemove', function(evt) {
        var mousePos = getMousePos(ctx.canvas, evt);
         $("#mouse").empty()
            .append("<li>x: " + mousePos.x + "</li>")
            .append("<li>y: " + mousePos.y + "</li>");
    }, false);



    $("#world").empty()
        .append("<li>x max: " + body.world.x_max + "</li>")
        .append("<li>y max: " + body.world.y_max + "</li>")
        .append("<li>x min: 0 </li>")
        .append("<li>y min: 0 </li>");

    doUpdate = false;
}

// called when a message arrives
function onMessageArrived(message) {

    console.log("onMessageArrived");

    var c = $("#map_layer");
    var ctx = c[0].getContext('2d');

    console.log(message.destinationName);

    var body = JSON.parse(message.payloadString)
    if (message.destinationName === 'game/position') {
        if(doUpdate) {

            createWorld(ctx, body)

        } else {

            updatePoints(ctx, body.points)

            var robot = body.robot
            drawRobot(robot.x, robot.y, robot.r, max_x, max_y)

            $("#position").empty()
                .append("<li>x: " + robot.x + "</li>")
                .append("<li>y: " + robot.y + "</li>")
                .append("<li>r: " + robot.r + "</li>");

            var score = getScore(body.points);
             $("#score").empty()
                .append("<li>max: " + score.max + "</li>")
                .append("<li>current: " + score.current + "</li>");

        }
    }

    if (message.destinationName === 'robot/state') {

         $("#state").empty()
            .append("<li>angle: " + body.angle + "</li>")
            .append("<li>left motor: " + body.left_motor + "</li>")
            .append("<li>right motor: " + body.right_motor + "</li>");
    }


}


// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});
