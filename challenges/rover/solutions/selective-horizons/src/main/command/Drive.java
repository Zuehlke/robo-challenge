package main.command;

public class Drive extends Command {

    public static final int MAX_DISTANCE = 5000;

    private int mDistance;

    public Drive(int distance) {
        mDistance = distance;
    }

    public int getDistance() {
        return mDistance;
    }
}
