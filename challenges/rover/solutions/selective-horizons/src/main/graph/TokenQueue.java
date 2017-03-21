package main.graph;

import main.pathfinder.Cost;

import java.util.HashSet;
import java.util.LinkedList;

public class TokenQueue {

    LinkedList<Token> mTokens;
    HashSet<Integer> mVisitedX;

    public TokenQueue(Token[] tokens) {
        mTokens = new LinkedList<>();
        mVisitedX = new HashSet<>();

        for (Token token : tokens) {
            if (token.getValue() > 0) {
                mTokens.add(token);
            }
        }
    }

    public synchronized Token dequeueToken(Point start, double direction) {
        double minCost = Double.POSITIVE_INFINITY;
        Token closestToken = null;

        for (Token token : mTokens) {
            double cost = Cost.computeCost(start, token.getPosition(), mTokens, direction);
            if (cost < minCost && !mVisitedX.contains(token.getPosition().getX())) {
                minCost = cost;
                closestToken = token;
            }
        }

        return closestToken;
    }

    /*public synchronized void removeTokenAtPosition(Point pos) {
        for (Token token : mTokens) {
            if (token.getPosition().getX() == pos.getX() && token.getPosition().getY() == pos.getY()) {
                mTokens.remove(token);
            }
        }
    }*/

    public synchronized void visitedToken(Point pos) {
        mVisitedX.add(pos.getX());
    }
}