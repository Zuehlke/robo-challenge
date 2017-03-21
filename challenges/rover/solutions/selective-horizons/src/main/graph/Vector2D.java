package main.graph;

public class Vector2D {
    double mX;
    double mY;

    public Vector2D(double x, double y) {
        mX = x;
        mY = y;
    }

    public double getX() {
        return mX;
    }

    public double getY() {
        return mY;
    }

    public Vector2D add(Vector2D o) {
        return new Vector2D(mX + o.getX(), mY + o.getY());
    }

    public Vector2D subtract(Vector2D o) {
        return new Vector2D(mX - o.getX(), mY - o.getY());
    }

    public double getSquaredNorm() {
        return mX*mX + mY*mY;
    }

    public double getNorm() {
        return Math.sqrt(getSquaredNorm());
    }

    public Vector2D scalarMult(double a) {
        return new Vector2D(a*mX, a*mY);
    }

    public Vector2D normalize() {
        double norm = getNorm();
        return scalarMult(1/ norm);
    }
}
