package main.control;

import main.command.*;
import main.graph.*;
import main.network.Client;
import main.state.GameState;
import main.state.RobotState;

import java.util.List;

public class Controller implements Client.StateListener {

    private static final int TOKEN_RADIUS = 5;
    private static final int ROTATING_TIME = 13000;
    private static final int GRACE_DISTANCE = 80;

    private Client mClient;
    private TokenQueue mTokens;

    private Point mNextPoint;
    private Point mLastPoint;
    private Point mCurrentPosition;

    private int mRobotRadius;
    private double mOrientation = 0;
    private double mNextCorrectionDistance = 50;

    private boolean mIsRotating = false;
    private boolean mIsBackwards = false;

    private static double toDegrees(double rad) {
        return (rad > 0 ? rad : (2 * Math.PI + rad)) * 360 / (2 * Math.PI);
    }

    private static final double positiveAngle(double angle) {
        return angle > 0 ? angle : 360 + angle;
    }

    public Controller(Client client) {
        mClient = client;
    }

    public void start() {
        mNextPoint = mTokens.dequeueToken(mCurrentPosition, mOrientation).getPosition();
        mClient.setStateListener(this);

        if (mNextPoint != null) {
            accelerateToPoint();
        }
    }

    public void setTokens(TokenQueue tokens, Point startingPoint) {
        mTokens = tokens;
        mLastPoint = startingPoint;
        mCurrentPosition = startingPoint;
    }

    private void computeOrientation() {
        Vector2D last = mLastPoint.toVector();
        Vector2D current = mCurrentPosition.toVector();

        Vector2D direction = current.subtract(last);
        if (direction.getSquaredNorm() >= 50 * 50) {
            System.out.println("Expected orientation: "+mOrientation);
            mOrientation = positiveAngle(toDegrees(Math.atan2(direction.getY(), direction.getX())));

            if (mIsBackwards) {
                mOrientation = (mOrientation + 180) % 360;
            }
            System.out.println("Estimated orientation: "+mOrientation);
        }
    }

    private void accelerateToPoint() {
        mIsBackwards = false;
        Vector2D next = mNextPoint.toVector();
        Vector2D current = mCurrentPosition.toVector();

        Vector2D direction = next.subtract(current);
        double newAngle = toDegrees(Math.atan2(direction.getY(), direction.getX()));

        System.out.println("Next point: "+mNextPoint.getX()+"/"+mNextPoint.getY());
        System.out.println(direction.getX()+"/"+direction.getY()+": new angle: " +newAngle);

        Command rotation;
        Command drive;

        int dAngle = (int)(newAngle - mOrientation);
        dAngle = dAngle > 0 ? dAngle : 360 + dAngle;

        int effectiveAngle = 0;
        System.out.println("Current orientation: "+mOrientation);

        if (dAngle >= 0 && dAngle <= 180) {
            if (dAngle <= 90) {
                effectiveAngle = dAngle;
                rotation = new LeftRotation(effectiveAngle);
                drive = new ForwardDrive(Drive.MAX_DISTANCE);
                System.out.println("rotating left by "+effectiveAngle+" degrees");
            } else {
                effectiveAngle = 180 - dAngle;
                rotation = new RightRotation(effectiveAngle);
                drive = new BackwardDrive(Drive.MAX_DISTANCE);
                System.out.println("rotating right by "+effectiveAngle+" degrees");
            }
        }
        else {
            if (dAngle >= 270) {
                effectiveAngle = 360 - dAngle;
                rotation = new RightRotation(effectiveAngle);
                drive = new ForwardDrive(Drive.MAX_DISTANCE);
                System.out.println("rotating right by "+(360 - dAngle)+" degrees");
            } else {
                effectiveAngle = dAngle - 180;
                rotation = new LeftRotation(effectiveAngle);
                drive = new BackwardDrive(Drive.MAX_DISTANCE);
                System.out.println("rotating left by "+(dAngle - 180)+" degrees");
            }
        }

        mClient.sendCommand(rotation);
        mIsRotating = true;

        new java.util.Timer().schedule(
                new java.util.TimerTask() {
                    @Override
                    public void run() {
                        mIsRotating = false;
                        mLastPoint = mCurrentPosition;

                        mClient.sendCommand(drive);
                        System.out.println(drive.getClass());

                        if (drive.getClass() == ForwardDrive.class) {
                            mOrientation = newAngle;
                        } else {
                            mIsBackwards = true;
                            mOrientation = (newAngle + 180) % 360;
                            System.out.println("rotated. estimated orientation: "+mOrientation);
                        }
                    }
                },
                effectiveAngle * ROTATING_TIME / 360 + 500
        );
    }

    private boolean isAtTarget() {
        Vector2D next = mNextPoint.toVector();
        Vector2D current = mCurrentPosition.toVector();

        double distanceSquared = next.subtract(current).getSquaredNorm();
        double targetDist = mRobotRadius + TOKEN_RADIUS;

        return (distanceSquared < targetDist * targetDist);
    }

    private void switchToNextPoint() {
        mClient.sendCommand(new Stop());
        mLastPoint = mNextPoint;
        mTokens.visitedToken(mLastPoint);

        Token next = mTokens.dequeueToken(mCurrentPosition, mOrientation);
        mNextCorrectionDistance = 50;

        if (next != null) {
            mNextPoint = next.getPosition();
            System.out.println("Going to "+mNextPoint.getX()+"/"+mNextPoint.getY());
            accelerateToPoint();

            // skip if we reached multiple points at once
            if (isAtTarget()) {
                mNextPoint = mTokens.dequeueToken(mCurrentPosition, mOrientation).getPosition();
            }
        }
    }

    private void courseCorrection() {
        mClient.sendCommand(new Stop());
        accelerateToPoint();
        mNextCorrectionDistance += GRACE_DISTANCE;
    }

    private boolean isOnCourse() {
        if (mLastPoint != null) {
            Vector2D currPos = mCurrentPosition.toVector();
            Vector2D lastPos = mLastPoint.toVector();
            Vector2D nextPos = mNextPoint.toVector();

            Vector2D currentDirection = currPos.subtract(lastPos);

            // only check if the rover has a sufficient distance
            if (currentDirection.getSquaredNorm() > mNextCorrectionDistance * mNextCorrectionDistance) {
                Vector2D desiredDirection = nextPos.subtract(currPos);

                double distance = desiredDirection.getNorm();
                double ratio = distance / currentDirection.getNorm();

                Vector2D projectedPoint = currentDirection.scalarMult(ratio).add(currPos);
                Vector2D difference = projectedPoint.subtract(nextPos);

                double pickupRadius = mRobotRadius + TOKEN_RADIUS;

                if (difference.getSquaredNorm() < pickupRadius * pickupRadius) {
                    return true;
                } else {
                    return false;
                }
            }
        }

        return true;
    }

    @Override
    public void receivedGameState(GameState state) {
        RobotState robotState = state.getRobotState();
        mCurrentPosition = new Point(robotState.getX(), robotState.getY());
        mRobotRadius = robotState.getRadius();

        boolean atTarget = isAtTarget();
        if (atTarget) {
            switchToNextPoint();
        }
        if (!mIsRotating) {
            if (!atTarget) {
                computeOrientation();

                if (!isOnCourse()) {
                    courseCorrection();
                }
            }
        }
    }

    @Override
    public void receivedRobotState(String state) {

    }

    @Override
    public void receivedCollected(List<Point> points) {
        for (Point pos : points) {
            mTokens.visitedToken(pos);
        }
    }
}