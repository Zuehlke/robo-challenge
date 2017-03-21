package main.state;

public class RobotState {

    private int mRadius;
    private int mXPos;
    private int mYPos;

    public RobotState(int r, int x, int y) {
        mRadius = r;
        mXPos = x;
        mYPos = y;
    }

    public int getRadius() {
        return mRadius;
    }

    public int getX() {
        return mXPos;
    }

    public int getY() {
        return mYPos;
    }
}
