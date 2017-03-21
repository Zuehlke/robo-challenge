package main.graph;

public class Token {
    private Point mPosition;
    private int mRadius;

    private int mValue;

    public Token(Point position, int radius, int value) {
        mPosition = position;
        mRadius = radius;
        mValue = value;
    }

    public Point getPosition() {
        return mPosition;
    }

    public int getValue() {
        return mValue;
    }
}
