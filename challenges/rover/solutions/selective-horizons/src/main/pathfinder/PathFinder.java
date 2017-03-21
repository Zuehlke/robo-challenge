package main.pathfinder;

import main.graph.*;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

import static java.util.ArrayList.*;

public class PathFinder {

    private Topology mTopology;
    private Point mStartPosition;

    public PathFinder(Topology topology, Point startPosition) {
        mTopology = topology;
        mStartPosition = startPosition;
    }

    public Path computePath(int maxSteps) {
        Path path = new Path();
        List<Token> tokens = Arrays.asList(mTopology.getTokens().clone());
        LinkedList<Token> unvisited = new LinkedList<>(tokens);

        Vector2D currentPosition = mStartPosition.toVector();

        for (int i = 0; i < maxSteps; i++) {
            double minDistance = Integer.MAX_VALUE;
            Token closestToken = null;

            for (Token token : unvisited) {
                if (token.getValue() > 0) {
                    Vector2D pos = token.getPosition().toVector();
                    double distance = pos.subtract(currentPosition).getSquaredNorm();

                    if (distance < minDistance) {
                        closestToken = token;
                        minDistance = distance;
                    }
                }
            }

            if (closestToken != null) {
                path.addPoint(closestToken.getPosition());
                unvisited.remove(closestToken);
                currentPosition = closestToken.getPosition().toVector();
            }
        }

        return path;
    }


    /*class Branch{
      public LinkedList<Token> potential;
      public int score;

      public branch(LinkedList<Token> Potential, int Score){
          score = Score;
          potential = Potential;
      }

      public double getScore(){
        return score;
      }

      public LinkedList<Token> getBranchPath(){
        return potential;
      }
    }



    public LinkedList<Token> shortList(LinkedList<Token> toCut, Token root, double rootAngle){
      LinkedList<Token> cutList;
      double mincost;
      int tempcost = 0;
      int index = -1;
      for(int counter = 0; counter < 5; counter++){
        mincost = Integer.MAX_VALUE;
        for(Token newElement:toCut){
          tempcost = cost.timeCost(root, newElement, rootAngle)
          if(mincost > tempcost){
            mincost = tempcost;
            index = shortList.indexOf(newElement);
          }
        }
        if(index > 0){
          cutList.add(toCut.get(index));
          toCut.remove(index);
        }
      }
      return sortedList;
    }

    public Path computePath(int maxTime) {
      Path path = new Path;
      List<Token> tokens = Arrays.asList(mTopology.getTokens().clone());
      LinkedList<Token> unvisitedminus = new LinkedList<>(tokens);
      LinkedList<Token> unvisited = new LinkedList<>(tokens);

      for(Token negativTest:unvisitedminus){
        if(negativTest.getValue()>0){
          unvisited.add(negativTest);
        }
      }
      Point origin = new Point(0,0);
      Token root = new Token(origin,1,0);
      unvisited = shortList(unvisited,root,0);

      int endscore = 0;
      Branch endtree;
      Branch computationBranch;
      Token firstOne;

      for(Token testingbranch : unvisited){
        LinkedList<Token> unvisitedOrig = new LinkedList<>(tokens);
        unvisitedOrig.remove(testingbranch);
        double rightAngle = Math.acos(((testingbranch.normalize()).getX()));
        double timeEstimate = cost.timeCost(origin, testingbranch, rightAngle);
        computationBranch = growing(unvisitedOrig, origin, rigthAngle ,3000 - timeEstimate);
        if(computationBranch.getScore() > endscore){
          endtree = computationBranch;
          endscore = computationBranch.getScore();
          firstOne = testingbranch;
        }
      }
      path = (computationBranch.getBranchPath()).add(firstOne);
      return path;
    }
    public Branch growing(LinkedList<Token> possibiblities, Point root, double angle, int timeleft){
      //TODO: Impelemnting recursive growth
<<<<<<< HEAD
    }*/
}
