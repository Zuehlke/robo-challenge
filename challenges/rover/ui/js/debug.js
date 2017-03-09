var client = new Paho.MQTT.Client(location.hostname, Number(9001), guid());


var viewState = { robotState: {}, robotPosition: {}, xmax: 1280, ymax: 960 }

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

// called when the client connects
function onConnect() {
    // Once a connection has been made, make a subscription.
    console.log("onConnect");
    client.subscribe("robot/state");
    client.subscribe("robot/position");
}

// called when the client loses its connection
function onConnectionLost(responseObject) {
    if (responseObject.errorCode !== 0) {
        console.log("onConnectionLost:"+responseObject.errorMessage);
    }
}

function drawRobot(robot, x_max, y_max) {
    var c = $("#debug_layer");
    var ctx = c[0].getContext('2d');

    var x = robot.x;
    var y = robot.y;
    var r = robot.r;

    ctx.canvas.height = y_max;
    ctx.canvas.width = x_max;

    ctx.translate(0, y_max);
    ctx.scale(1, -1);

    ctx.clearRect(0, 0, x_max, y_max);

    ctx.beginPath();
    ctx.lineWidth = 1;

    ctx.arc(x, y, r, 2 * Math.PI, false);
    ctx.strokeStyle = "#000000";
    ctx.stroke();



    ctx.beginPath();

    ctx.arc(x, y, 2, 2 * Math.PI, false);
    ctx.fillStyle = "#000000";
    ctx.fill();

    ctx.beginPath();

    ctx.moveTo(x, y);
    ctx.lineTo(x, y - r);
    ctx.lineTo(x, y + r);
    ctx.moveTo(x, y);
    ctx.lineTo(x - r , y);
    ctx.lineTo(x + r , y);

    ctx.stroke();

    var cx = x_max / 2;
    var cy = y_max / 2;
    var l = 50;

    ctx.beginPath();

    ctx.moveTo(cx, cy);
    ctx.lineTo(cx, cy - l);
    ctx.lineTo(cx, cy + l);

    ctx.moveTo(cx, cy);
    ctx.lineTo(cx - l , cy);
    ctx.lineTo(cx + l , cy);


    ctx.stroke();


}



function onMessageArrived(message) {


    var body = JSON.parse(message.payloadString);
    if (message.destinationName === 'robot/position') {
        viewState.robotPosition = body;
        drawRobot(body, viewState.xmax, viewState.ymax)
    }

    if (message.destinationName === 'robot/state') {
        viewState.robotState = body;
    }

}

var notice = new Vue({
    el: '#notice',
    data: viewState
});

// set callback handlers
client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});