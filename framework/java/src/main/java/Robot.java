import ev3dev.hardware.motor.EV3LargeRegulatedMotor;
import ev3dev.hardware.port.MotorPort;
import ev3dev.hardware.port.SensorPort;
import ev3dev.hardware.sensor.SensorMode;
import ev3dev.hardware.sensor.SensorModes;
import ev3dev.hardware.sensor.ev3.EV3ColorSensor;
import ev3dev.hardware.sensor.ev3.EV3UltrasonicSensor;
import lejos.robotics.SampleProvider;

import java.util.ArrayList;
import java.util.List;

/**
 * Java robot example
 */
public class Robot {


    // default sleep timeout in sec
    private static final double DEFAULT_SLEEP_TIMEOUT_IN_SEC = 0.1;

    // default speed
    private static final int DEFAULT_SPEED = 250;

    // default threshold distance
    private static final int DEFAULT_THRESHOLD_DISTANCE = 90;

    private EV3LargeRegulatedMotor rightMotor;
    private EV3LargeRegulatedMotor leftMotor;
    private List<EV3LargeRegulatedMotor> motors = new ArrayList<>();

    private EV3UltrasonicSensor ultrasonicSensor;
    private EV3ColorSensor colorSensor;

    public Robot() {

        //
        // Setup
        //

        System.out.println("Setting up...");

        // motors
        rightMotor = new EV3LargeRegulatedMotor(MotorPort.A);
        System.out.println("right motor connected: " + rightMotor);

        leftMotor = new EV3LargeRegulatedMotor(MotorPort.B);
        System.out.println("left motor connected: " + leftMotor);

        motors.add(rightMotor);
        motors.add(leftMotor);
        rightMotor.resetTachoCount();
        leftMotor.resetTachoCount();

        // sensors
        colorSensor = new EV3ColorSensor(SensorPort.S4);
        System.out.println("color sensor connected: " + colorSensor);
        colorSensor.setCurrentMode("COL-REFLECT");

        ultrasonicSensor = new EV3UltrasonicSensor(SensorPort.S2);
        System.out.println("ultrasonic sensor connected: " + ultrasonicSensor);
        ultrasonicSensor.setCurrentMode("US-DIST-CM");

    }

    //
    // Robot functionality
    //

    public void backward() {
        for (EV3LargeRegulatedMotor m: motors) {
            m.backward();
        }
    }

    public void forward() {
        for (EV3LargeRegulatedMotor m: motors) {
            m.forward();
        }
    }

    public void setSpeed(int speed) {
        for (EV3LargeRegulatedMotor m: motors) {
            m.setSpeed(speed);
        }
    }

    public void brake() {
        for (EV3LargeRegulatedMotor m: motors) {
            m.stop();
        }
    }

    public void turn() {
        leftMotor.stop();
        float pos = rightMotor.getPosition();

        // new absolute position
        float absPos = pos + 500;

        while (Math.abs(rightMotor.getPosition() - absPos) > 10) {
            // turn to new position

            // stop when object detected
            if(getDistance(ultrasonicSensor) < DEFAULT_THRESHOLD_DISTANCE) {
                break;
            }
        }

        setSpeed(DEFAULT_SPEED);
        forward();

    }

    public void tearDown() {
        System.out.println("Tearing down...");

        for (EV3LargeRegulatedMotor m : motors) {
            m.stop();
            m.resetTachoCount();
        }
    }

    public void runLoop() {

        System.out.println("color value: " + getColorReflect(colorSensor));
        System.out.println("ultrasonic value: " + getDistance(ultrasonicSensor));
        System.out.println("motor positions (r, l): " + rightMotor.getPosition() + ", "  + leftMotor.getPosition());

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

    private int getDistance(EV3UltrasonicSensor ultrasonicSensor) {
        final SampleProvider sp = ultrasonicSensor.getDistanceMode();
        float [] sample = new float[sp.sampleSize()];
        sp.fetchSample(sample, 0);
        return (int)sample[0];
    }

    private int getColorReflect(EV3ColorSensor colorSensor) {
        final SampleProvider sp = colorSensor.getColorIDMode();
        float [] sample = new float[sp.sampleSize()];
        sp.fetchSample(sample, 0);
        return (int)sample[0];
    }

}
