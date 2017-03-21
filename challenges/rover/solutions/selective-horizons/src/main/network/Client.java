package main.network;

import main.command.*;
import main.graph.Point;
import main.graph.Topology;

import main.state.GameState;
import main.state.RobotState;
import org.eclipse.paho.client.mqttv3.*;
import org.json.*;

import java.util.List;
import java.util.UUID;

public class Client implements MqttCallback {

    public interface ClientListener {
        void receivedStartMessage();
        void receivedTopology(Topology topology, Point startPosition);
    }

    public interface StateListener {
        void receivedGameState(GameState state);
        void receivedRobotState(String state);
        void receivedCollected(List<Point> points);
    }

    //-----------------------------//
    //  Constants                  //
    //-----------------------------//
    private static final String TEAM_NAME         = "selective";
    private static final String TOPIC_MAIN        = "players/" + TEAM_NAME;
    private static final String TOPIC_ANY         = TOPIC_MAIN + "/#";
    private static final String TOPIC_GAME        = TOPIC_MAIN + "/game";
    private static final String TOPIC_INCOMING    = TOPIC_MAIN + "/incoming";

    private static final String TOPIC_ROBOT_STATE   = "robot/state";
    private static final String TOPIC_ROBOT_PROCESS = "robot/process";

    private static final String KEY_COMMAND = "command";
    private static final String KEY_POINTS  = "points";

    private static final String CMD_REGISTER = "register";
    private static final String CMD_START = "start";

    //-----------------------------//
    //  Fields                     //
    //-----------------------------//
    private String mBrokerHost;

    private MqttClient mMqttSender;
    private MqttClient mMqttListener;

    private ClientListener mClientListener;
    private StateListener  mStateListener;

    private boolean mReceivedTopology;

    public Client(String brokerHost) {
        mBrokerHost = brokerHost;

        try {
            mMqttSender = createMqttClient();
            mMqttListener = createMqttClient();

            mMqttListener.setCallback(this);
            mMqttListener.subscribe(TOPIC_ANY);
            mMqttListener.subscribe(TOPIC_ROBOT_STATE);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void setClientListener(ClientListener listener) {
        mClientListener = listener;
    }

    public void setStateListener(StateListener listener) {
        mStateListener = listener;
    }

    //-----------------------------//
    //  Helper methods             //
    //-----------------------------//
    private MqttClient createMqttClient() throws MqttException {
        MqttClient mqtt = new MqttClient(mBrokerHost, UUID.randomUUID().toString());
        mqtt.connect(new MqttConnectOptions());
        return mqtt;
    }

    private void publishJson(String topic, JSONObject object) {
        MqttMessage message = new MqttMessage();
        message.setPayload(object.toString().getBytes());

        try {
            mMqttSender.publish(topic, message);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    //-----------------------------//
    //  Public methods             //
    //-----------------------------//
    public void register() {
        JSONObject object = new JSONObject();
        object.put(KEY_COMMAND, CMD_REGISTER);
        publishJson(TOPIC_MAIN, object);
    }

    public void start() {
        JSONObject object = new JSONObject();
        object.put(KEY_COMMAND, CMD_START);
        publishJson(TOPIC_MAIN, object);
    }

    public void sendCommand(Command cmd) {
        JSONObject object = MessageBuilder.buildCommandMessage(cmd);
        publishJson(TOPIC_ROBOT_PROCESS, object);
    }

    //-----------------------------//
    //  MQTT methods               //
    //-----------------------------//
    @Override
    public void connectionLost(Throwable throwable) {
        System.out.println(throwable);
    }

    @Override
    public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
        JSONObject obj = new JSONObject(new String(mqttMessage.getPayload()));

        if (topic.equals(TOPIC_INCOMING)) {
            String command = obj.getString(KEY_COMMAND);

            if (command.equals(CMD_START)) {
                mClientListener.receivedStartMessage();
            } else if (command.equals("finish")) {
                sendCommand(new Stop());
            }
        }
        else if (topic.equals(TOPIC_GAME)) {
            GameState state = MessageParser.parseGameState(obj);
            if (mStateListener != null)
                mStateListener.receivedGameState(state);

            if (!mReceivedTopology) {
                JSONArray points  = obj.getJSONArray(KEY_POINTS);
                Topology topology = MessageParser.parseTopology(points);

                RobotState robotState = state.getRobotState();
                Point position = new Point(robotState.getX(), robotState.getY());
                mClientListener.receivedTopology(topology, position);

                mReceivedTopology = true;
            } else {
                JSONArray points  = obj.getJSONArray(KEY_POINTS);
                List<Point> list = MessageParser.parseTokens(points);

                if (mStateListener != null)
                    mStateListener.receivedCollected(list);
            }
        }
        else if (topic.equals(TOPIC_ROBOT_STATE)) {
            if (mStateListener != null)
                mStateListener.receivedRobotState(obj.toString());
        }
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {

    }
}

