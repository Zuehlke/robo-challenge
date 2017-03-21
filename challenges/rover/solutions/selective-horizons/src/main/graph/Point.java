package main.graph;

public class Point {
    int mX;
    int mY;

    public Point(int x, int y) {
        mX = x;
        mY = y;
    }

    public int getX() {
        return mX;
    }

    public int getY() {
        return mY;
    }

    public Vector2D toVector() {
        return new Vector2D(mX, mY);
    }
}
