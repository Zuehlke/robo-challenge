package main.network;

import main.graph.Point;
import main.graph.Vector2D;
import main.graph.Token;
import main.graph.Topology;
import main.state.GameState;
import main.state.RobotState;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.LinkedList;

public class MessageParser {

    public static GameState parseGameState(JSONObject obj) {
        JSONObject robotObj = obj.getJSONObject("robot");
        int r = robotObj.getInt("r");
        int x = robotObj.getInt("x");
        int y = robotObj.getInt("y");

        RobotState robotState = new RobotState(r, x, y);

        return new GameState(robotState, null);
    }

    public static Topology parseTopology(JSONArray array) {
        int nTokens = array.length();
        Token[] tokens = new Token[nTokens];

        for (int i = 0; i < nTokens; i++) {
            JSONObject point = array.getJSONObject(i);

            int x = point.getInt("x");
            int y = point.getInt("y");
            int r = point.getInt("r");
            int score = point.getInt("score");

            tokens[i] = new Token(new Point(x, y), r, score);
        }

        return new Topology(tokens);
    }

    public static LinkedList<Point> parseTokens(JSONArray array) {
        int nTokens = array.length();
        LinkedList<Point> list = new LinkedList<>();

        for (int i = 0; i < nTokens; i++) {
            JSONObject point = array.getJSONObject(i);

            int x = point.getInt("x");
            int y = point.getInt("y");
            boolean collected = point.getBoolean("collected");

            if (collected) {
                list.add(new Point(x,y));
            }
        }

        return list;
    }
}
