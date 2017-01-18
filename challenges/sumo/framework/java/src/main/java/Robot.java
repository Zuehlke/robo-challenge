import ev3dev.hardware.motor.EV3LargeRegulatedMotor;
import ev3dev.hardware.port.MotorPort;
import ev3dev.hardware.port.SensorPort;
import ev3dev.hardware.sensor.ev3.EV3ColorSensor;
import ev3dev.hardware.sensor.ev3.EV3UltrasonicSensor;
import lejos.robotics.SampleProvider;
import lejos.utility.Delay;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * Java robot example
 */
public class Robot {


    // default sleep timeout in sec
    private static final int DEFAULT_SLEEP_TIMEOUT_IN_MSEC = 100;

    // default speed
    private static final int DEFAULT_SPEED = 600;

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


        leftMotor.resetTachoCount();
        rightMotor.resetTachoCount();


        motors.add(rightMotor);
        motors.add(leftMotor);

        // sensors
        colorSensor = new EV3ColorSensor(SensorPort.S4);
        System.out.println("color sensor connected: " + colorSensor);

        ultrasonicSensor = new EV3UltrasonicSensor(SensorPort.S1);
        System.out.println("ultrasonic sensor connected: " + ultrasonicSensor);

    }

    //
    // Robot functionality
    //

    public void backward() {
        for (EV3LargeRegulatedMotor m : motors) {
            m.backward();
        }
    }

    public void forward() {
        for (EV3LargeRegulatedMotor m : motors) {
            m.forward();
        }
    }

    public void setSpeed(int speed) {
        for (EV3LargeRegulatedMotor m : motors) {
            // possible workaround for speed regulation
            // m.setStringAttribute("speed_regulation", "on");
            m.setSpeed(speed);
        }
    }


    public void brake() {
        for (EV3LargeRegulatedMotor m : motors) {
            m.stop();
        }
    }

    public void turn()  {
        leftMotor.stop();
        float pos = getPosition(rightMotor);

        // new absolute position
        float absPos = pos + 500;
        rightMotor.forward();

        while (Math.abs(getPosition(rightMotor) - absPos) > 10) {
            // turn to new position

            // stop when object detected
            if (getDistance(ultrasonicSensor) < DEFAULT_THRESHOLD_DISTANCE) {
                break;
            }
        }

        setSpeed(DEFAULT_SPEED);
        forward();

    }

    public void tearDown() {
        System.out.println("Tearing down...");

        for (EV3LargeRegulatedMotor m : motors) {
            m.setSpeed(0);
            m.forward();
            m.resetTachoCount();
        }
    }

    public void runLoop() {

        System.out.println("color value: " + getColorReflect(colorSensor));
        System.out.println("ultrasonic value: " + getDistance(ultrasonicSensor));
        System.out.println("motor positions (r, l): " + getPosition(rightMotor) + ", " + getPosition(leftMotor));


        // found obstacle
        if (getDistance(ultrasonicSensor) < DEFAULT_THRESHOLD_DISTANCE) {

            brake();

            // drive backwards
            setSpeed(DEFAULT_SPEED / 2);
            backward();

            float newPos = getPosition(rightMotor) - 200;
            long timeout = new Date().getTime();
            while (getPosition(rightMotor) - newPos > 10) {
                // wait until robot has reached the new position or timeout (milliseconds) has expired
                if (new Date().getTime() - timeout > 5000) break;
            }

            // turn
            turn();


        } else {
            forward();
        }

    }

    private int getDistance(EV3UltrasonicSensor ultrasonicSensor) {
        final SampleProvider sp = ultrasonicSensor.getDistanceMode();
        float[] sample = new float[sp.sampleSize()];
        sp.fetchSample(sample, 0);
        return (int) sample[0];
    }

    private int getColorReflect(EV3ColorSensor colorSensor) {
        final SampleProvider sp = colorSensor.getRedMode();
        float[] sample = new float[sp.sampleSize()];
        sp.fetchSample(sample, 0);
        return (int) sample[0];
    }

    // workaround: position does not work
    private int getPosition(EV3LargeRegulatedMotor motor) {
        return motor.getIntegerAttribute("position");
    }

    public static void main(String[] args){

        System.out.println("Run robot, run!");

        Robot robot = new Robot();

         attachShutDownHook(robot);

        try {
            robot.setSpeed(DEFAULT_SPEED);
            robot.forward();

            while (true) {
                robot.runLoop();
                Delay.msDelay(DEFAULT_SLEEP_TIMEOUT_IN_MSEC);
            }

        } catch (Exception ex) {
            robot.tearDown();
        }
    }

    // handling exits
    private static void attachShutDownHook(final Robot robot) {
        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                robot.tearDown();
            }
        });
    }

}
