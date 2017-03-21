package main.pathfinder;

import main.graph.*;

import java.util.List;

public class Cost {

    public static double computeCost(Point start, Point end, List<Token> tokens, double orientation) {
        Vector2D startVec = start.toVector();
        Vector2D endVec = end.toVector();

        Vector2D distance = startVec.subtract(endVec);
        double distanceCost = distance.getNorm();

        double marginCost = 0;
        if (end.getY()<100 || end.getY() > 860) {
            marginCost += 200;
        } else if (end.getX() < 100 | end.getX() > 1180) {
            marginCost += 200;
        }

        double clusterBonus = 0;
        for (Token token : tokens) {
            double neighbourDist = token.getPosition().toVector().subtract(end.toVector()).getNorm();
            if (neighbourDist < 300) {
                clusterBonus = 300 - neighbourDist;
            }
        }

        //System.out.println("dist: "+distanceCost+", angle"+angleCost);
        return distanceCost + 0.6*marginCost - 0.6*clusterBonus;
    }

    public static double getDirection(Vector2D start, Vector2D end) {
        Vector2D difference = end.subtract(start);
        double angle = Math.atan2(difference.getY(), difference.getX());

        angle = angle > 0 ? angle : 360 + angle;
        return angle;
    }
}
