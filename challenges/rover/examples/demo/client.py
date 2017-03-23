import paho.mqtt.client as mqtt
import json, sys, time

SERVER = "127.0.0.1"
PORT = 1883

PLAYER_NAME = "demo"

WAIT_SEC = 15

timestamp = time.time()
started = False
dist = 0
mode = 0

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('players/' + PLAYER_NAME + '/#')
    client.subscribe('robot/state')

    # register
    client.publish('players/' + PLAYER_NAME, json.dumps({"command": "register"}))


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global started, dist, timestamp, mode
    #print(msg.topic)
    obj = json.loads(msg.payload.decode("utf-8"))



    # TODO: implement algorithm
    if msg.topic == 'players/' + PLAYER_NAME + '/incoming':

        if obj['command'] == 'start':
            client.publish('players/' + PLAYER_NAME, json.dumps({"command": "start"}))
            started = True

            client.publish('robot/process', json.dumps({"command": "forward", "args": 1000}))
            mode = 1

        if obj['command'] == 'finished':
            sys.exit(0)

    if msg.topic == 'robot/state' and started:
        ts = time.time() - timestamp
        print(ts)

        if mode == 0 and ts > WAIT_SEC:
            client.publish('robot/process', json.dumps({"command": "forward", "args": 1000}))
            timestamp = time.time()
            ts = time.time() - timestamp
            mode = 1

        if mode == 1 and ts > WAIT_SEC:
            client.publish('robot/process', json.dumps({"command": "left", "args": 90}))
            timestamp = time.time()
            ts = time.time() - timestamp
            mode = 0


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(SERVER, PORT, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
try:
    client.loop_forever()
except (KeyboardInterrupt, SystemExit):
    print("Tearing down...")
    client.disconnect()
    raise