package main.state;

public class GameState {

    private RobotState mRobotState;
    private World mWorld;

    public GameState(RobotState robot, World world) {
        mRobotState = robot;
        mWorld = world;
    }

    public RobotState getRobotState() {
        return mRobotState;
    }

    public World getWorld() {
        return mWorld;
    }
}
