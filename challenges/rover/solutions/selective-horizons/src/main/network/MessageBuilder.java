package main.network;

import main.command.*;

import org.json.JSONObject;

public class MessageBuilder {

    private static final String KEY_COMMAND = "command";
    private static final String KEY_ARGS    = "args";

    private static final String CMD_FORWARD  = "forward";
    private static final String CMD_BACKWARD = "backward";
    private static final String CMD_LEFT     = "left";
    private static final String CMD_RIGHT    = "right";
    private static final String CMD_STOP     = "stop";

    public static JSONObject buildCommandMessage(Command cmd) {
        JSONObject object = new JSONObject();

        if (cmd.getClass() == LeftRotation.class) {
            LeftRotation rotation = (LeftRotation) cmd;
            object.put(KEY_COMMAND, CMD_LEFT);
            object.put(KEY_ARGS, rotation.getAngle());
        }
        else if (cmd.getClass() == RightRotation.class) {
            RightRotation rotation = (RightRotation) cmd;
            object.put(KEY_COMMAND, CMD_RIGHT);
            object.put(KEY_ARGS, rotation.getAngle());
        }
        else if (cmd.getClass() == ForwardDrive.class) {
            ForwardDrive drive = (ForwardDrive) cmd;
            object.put(KEY_COMMAND, CMD_FORWARD);
            object.put(KEY_ARGS, drive.getDistance());
        }
        else if (cmd.getClass() == BackwardDrive.class) {
            BackwardDrive drive = (BackwardDrive) cmd;
            object.put(KEY_COMMAND, CMD_BACKWARD);
            object.put(KEY_ARGS, drive.getDistance());
        }
        else if (cmd.getClass() == Stop.class) {
            object.put(KEY_COMMAND, CMD_STOP);
        }

        return object;
    }
}
