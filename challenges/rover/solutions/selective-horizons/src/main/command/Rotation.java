package main.command;

public class Rotation extends Command {

    private int mAngle;

    public Rotation(int angle) {
        mAngle = angle;
    }

    public int getAngle() {
        return mAngle;
    }
}
