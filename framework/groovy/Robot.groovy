
@GrabResolver(name = "jitpack.io", root = "https://jitpack.io")
@Grab(group = "com.github.jabrena", module = "ev3dev-lang-java", version = "v0.2.0")
import ev3dev.hardware.motor.EV3LargeRegulatedMotor
import ev3dev.hardware.port.MotorPort
import ev3dev.hardware.port.SensorPort
import ev3dev.hardware.sensor.ev3.EV3ColorSensor
import ev3dev.hardware.sensor.ev3.EV3UltrasonicSensor
import lejos.robotics.SampleProvider
import lejos.utility.Delay

// default sleep timeout in sec
DEFAULT_SLEEP_TIMEOUT_IN_MSEC = 100

// default speed
DEFAULT_SPEED = 600

// default threshold distance
DEFAULT_THRESHOLD_DISTANCE = 90

println("Setting up...")

// motors
rightMotor = new EV3LargeRegulatedMotor(MotorPort.A)
System.out.println("right motor connected: " + rightMotor)

leftMotor = new EV3LargeRegulatedMotor(MotorPort.B);
System.out.println("left motor connected: " + leftMotor)

motors = [rightMotor, leftMotor]

leftMotor.resetTachoCount();
rightMotor.resetTachoCount();


// sensors
colorSensor = new EV3ColorSensor(SensorPort.S4)
println("color sensor connected: " + colorSensor)

ultrasonicSensor = new EV3UltrasonicSensor(SensorPort.S1)
println("ultrasonic sensor connected: " + ultrasonicSensor)

//
// Robot functionality
//

def backward() {
    for (m in motors) {
        m.backward();
    }
}

def forward() {
    for (m in motors) {
        m.forward();
    }
}

def speed(int new_speed) {
    for (m in motors) {
        // possible workaround for speed regulation
        // m.setStringAttribute("speed_regulation", "on");
        m.setSpeed(new_speed);
    }
}

def brake() {
    for (m in motors) {
        m.stop();
    }
}

def turn() {
    leftMotor.stop();
    float pos = getPosition(rightMotor);

    // new absolute position
    float absPos = pos + 500
    rightMotor.forward()

    while (Math.abs(getPosition(rightMotor) - absPos) > 10) {
        // turn to new position

        // stop when object detected
        if (getDistance(ultrasonicSensor) < DEFAULT_THRESHOLD_DISTANCE) {
            break
        }
    }

    speed(DEFAULT_SPEED)
    forward()
}

def tearDown() {
    println("Tearing down...")

    for (m in motors) {
        m.setSpeed(0);
        m.forward()
        m.resetTachoCount()
    }
}

def getDistance(ultrasonicSensor) {
    SampleProvider sp = ultrasonicSensor.getDistanceMode()
    float[] sample = new float[sp.sampleSize()]
    sp.fetchSample(sample, 0)
    return (int) sample[0]
}

def getColorReflect(colorSensor) {
    SampleProvider sp = colorSensor.getRedMode()
    float[] sample = new float[sp.sampleSize()]
    sp.fetchSample(sample, 0)
    return (int) sample[0]
}

// workaround: position does not work
def getPosition(motor) {
    return motor.getIntegerAttribute("position")
}


def runLoop() {

    println("color value: " + getColorReflect(colorSensor))
    println("ultrasonic value: " + getDistance(ultrasonicSensor))
    println("motor positions (r, l): " + getPosition(rightMotor) + ", " + getPosition(leftMotor))

    // found obstacle
    if (getDistance(ultrasonicSensor) < DEFAULT_THRESHOLD_DISTANCE) {

        brake()

        // drive backwards
        speed(300)
        backward()

        newPos = getPosition(rightMotor) - 200
        timeout = new Date().getTime()
        while (getPosition(rightMotor) - newPos > 10) {
            // wait until robot has reached the new position or timeout (milliseconds) has expired
            if (new Date().getTime() - timeout > 5000) {
                break
            }
        }

        // turn
        turn()

    } else {
        forward()
    }
}


def runRobot() {

    println("Run robot, run!")

    try {
        speed(DEFAULT_SPEED)
        forward()

        while (true) {
            runLoop()
            Delay.msDelay(DEFAULT_SLEEP_TIMEOUT_IN_MSEC)
        }

    } catch (Exception ex) {
        println(ex)
        tearDown()
    }
}

// add shutdown hook
addShutdownHook {
    tearDown()
}

//
// start the program
//
runRobot()
