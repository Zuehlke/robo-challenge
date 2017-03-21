package main.graph;

import java.util.LinkedList;

public class Path {
    private LinkedList<Point> mPoints;

    public Path() {
        mPoints = new LinkedList<>();
    }

    public boolean isEmpty() {
        return mPoints.isEmpty();
    }

    public Point dequeuePoint() {
        Point first = mPoints.getFirst();
        mPoints.removeFirst();

        return first;
    }

    public void addPoint(Point point) {
        mPoints.add(point);
    }
}
