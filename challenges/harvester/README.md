
# Autonomous Harvester

tbd


### Lego Mindstorms Robot
Make sure that the motors are connected to the following ouput pins:

- Right motor (EV3 large motor) -> Output pin A
- Left motor (EV3 large motor) -> Output pin B

The Robot Harvester uses only the Gyro sensor.

![main page](robot.jpg)

### Positional System
tbd


### Simulator
tbd

### UI
![main page](ui.png)

### Message Specification
tbd

#### Topic (Write): robot/process
tbd


    mosquitto_pub -h 127.0.0.1 -t robot/process -m '{"command": "forward", "args": [100]}'

Drive 100 tacho counts forward

    {"command": "forward", "args": [100]}

Drive 50 tacho counts backward

    {"command": "forward", "args": [100]}

#### Topic (Read): robot/done
tbd

#### Topic (Read): robot/state
tbd

    mosquitto_sub -h 127.0.0.1 -t robot/state

    {"angle": 100, "left_motor": -143, "right_motor": 345}

#### Topic (Read): game/state
tbd

