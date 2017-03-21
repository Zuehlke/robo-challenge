import org.eclipse.paho.client.mqttv3.*;
import org.json.*;
import java.util.UUID;

public class Client implements MqttCallback{

    private static final String PLAYER_NAME  = "Roger";


    private static final String BROKER = "tcp://10.10.10.30:1883";//"tcp://127.0.0.1:1883";

    /* You need two connections in order to send/receive messages simultaniously */
    private final MqttClient mqttSender;
    private final MqttClient mqttListener;

    private Client(MqttClient mqttListener, MqttClient mqttSender) {
        initialized = false;
        this.mqttListener = mqttListener;
        this.mqttSender = mqttSender;
    }

    public static void main(String[] args) {

        try {
            MqttClient listener = createMqttClient();
            MqttClient sender = createMqttClient();


            System.out.println("Connecting to broker: " + BROKER);

            listener.setCallback(new Client(listener, sender));

            listener.subscribe("players/" + PLAYER_NAME + "/#");
            listener.subscribe("robot/state");

            MqttMessage ready = new MqttMessage("{\"command\": \"register\"}".getBytes());
            sender.publish("players/" + PLAYER_NAME, ready);


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Override
    public void connectionLost(Throwable throwable) {
        System.out.println(throwable);
    }

    @Override
    public void messageArrived(String topic, MqttMessage mqttMessage) throws Exception {
        //System.out.println(topic);
        JSONObject obj = new JSONObject(new String(mqttMessage.getPayload()));

        if (topic.equals("players/Roger/game")){
            //System.out.println("r= " + obj.getJSONObject("robot").getInt("r"));

            initialized = true;

            //notRotatedLast = true;
            naiveInit(obj);

            naiveApproach(obj);

        };

        if (topic.equals("robot/state")){
            //System.out.println("r= " + obj.getJSONObject("robot").getInt("r"));
            rotation = obj.getInt("angle");
            //rotating = (obj.getInt("left_motor") - obj.getInt("rightmotor")) > 50;
        };

        if (topic.equals("players/Roger/incoming") && obj.get("command").equals("start")){

            MqttMessage start = new MqttMessage("{\"command\": \"start\"}".getBytes());
            mqttSender.publish("players/" + PLAYER_NAME, start);

        };

        if (topic.equals("players/Roger/incoming") && obj.get("command").equals("finished")){
            //System.out.println("finished successful");

        };


    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {

    }

    private static MqttClient createMqttClient() throws MqttException {
        MqttClient mqtt = new MqttClient(BROKER, UUID.randomUUID().toString());
        MqttConnectOptions connOpts = new MqttConnectOptions();
        mqtt.connect(connOpts);
        return mqtt;
    }


    private void naiveInit(JSONObject gamestate){
        goodPoints = new int[gamestate.getJSONArray("points").length()][5];

        JSONArray array = gamestate.getJSONArray("points");
        for (int i = 0; i < array.length(); i++) {
            JSONObject elem = (JSONObject) array.get(i);
            goodPoints[i][0] = elem.getInt("x");
            goodPoints[i][1] = elem.getInt("y");
            goodPoints[i][2] = elem.getInt("score");
            goodPoints[i][4] = 0;
            if (elem.getBoolean("collected")) {
                goodPoints[i][3] = 1;
            } else {
                goodPoints[i][3] = 0;

            }

        }
    }
    private void initCluster() {
        for (int i = 0; i < goodPoints.length; i++) {
            for (int j = 0; j < goodPoints.length; j++) {
                double newDistance = Math.sqrt((double) Math.abs(((goodPoints[i][0] - goodPoints[j][0])*(goodPoints[i][0] - goodPoints[j][0]) + (goodPoints[j][1] - goodPoints[i][0])*(goodPoints[j][1] - goodPoints[i][0]))));
                //System.out.println(newDistance);
                if (goodPoints[i][2] != -1 && goodPoints[i][3] == 0 && newDistance < 350) {
                    goodPoints[i][4] += 1;
                } else if (goodPoints[i][2] == -1 && newDistance < 150) {
                    goodPoints[i][4] -= 2;
                }
            }
        }
    }


    private void naiveApproach(JSONObject gamestate) throws Exception {

        int r = Math.floorMod((int)realGyro(),360);//gamestate.getJSONObject("robot").getInt("r");
        //System.out.println(GYRO_OFFSET);
        //rotating = Math.floorMod(prevRotation - r,360) > 10;
        //System.out.println(Math.floorMod(prevRotation - r,360));
        int x = gamestate.getJSONObject("robot").getInt("x");
        int y = gamestate.getJSONObject("robot").getInt("y");
        int goToX = nextX;
        int goToY = nextY;

        collected = true;
        for (int i = 0; i < goodPoints.length; i++) {
            if ((nextX == goodPoints[i][0] && nextY == goodPoints[i][1]) && 0 == goodPoints[i][3]) {
                collected = false;
            }
        }

        if((nextX == 0 && nextY == 0)){collected = true;};
        //System.out.println(collected);

        initCluster();
        int distance = Integer.MAX_VALUE;
        if (null != goodPoints && collected) {

            for (int i = 0; i < goodPoints.length; i++) {
                double newDistance = (double) Math.abs(((x - goodPoints[i][0])*(x - goodPoints[i][0]) + (goodPoints[i][1] - y)*(goodPoints[i][1] - y))) - (10 * goodPoints[i][4]);
                //System.out.println((10 * goodPoints[i][4]));
                if (goodPoints[i][2] != -1 && goodPoints[i][3] == 0 && newDistance < distance) {
                    nextX = goodPoints[i][0];
                    nextY = goodPoints[i][1];
                    distance = (int) newDistance;
                }
            }
        }


        /*MqttMessage start = new MqttMessage("{\"command\": \"start\"}".getBytes());
        sender.publish("players/" + PLAYER_NAME, start);*/
        double angle = Math.floorMod((int)((180./Math.PI) * Math.atan2((double) (y - nextY) , (double) (nextX - x))),360);
        double alpha = Math.floorMod((int)(r - angle),360);
        if (rotating <= 0 && dfwd <= 0) {
            int intAlpha = Math.floorMod((int) alpha, 360);


                double myDistance = Math.abs((double) ((x - nextX)*(x - nextX) + (nextY - y)*(nextY - y)));

            //check what to do next
            //System.out.println(alpha);
            if (((intAlpha > 10 && intAlpha < 170 ) || (intAlpha > 190 && intAlpha < 350)) && myDistance > 20 && notRotatedLast) {

                JSONObject stopObj = new JSONObject();
                stopObj.put("command", "stop");
                MqttMessage stop = new MqttMessage(stopObj.toString().getBytes());
                mqttSender.publish("robot/process", stop);

                //set gyro

                lastX = CurrentX;
                lastY = CurrentY;
                CurrentX = x;
                CurrentY = y;

                weightedGyro(driveForward);

                prevDriveForward = driveForward;

                //System.out.println("!" + myGyro( driveForward) + " / " + Math.floorMod(rotation, 360) + " " + driveForward);


                //System.out.println(lastX + " " + lastY + " " + CurrentX + " " + CurrentY + " rot = " + Math.floorMod(rotation,360) + "    " + Math.floorMod((int)((180./Math.PI) * Math.atan2((double) (lastY - CurrentY) , (double) (CurrentX - lastX))),360));


                //rotate left or right
                if (intAlpha < 90) {
                    JSONObject rotObj = new JSONObject();
                    rotObj.put("command", "left");
                    rotObj.put("args", (int)(1.05*(double)intAlpha));

                    MqttMessage rotate = new MqttMessage(rotObj.toString().getBytes());
                    mqttSender.publish("robot/process", rotate);
                    rotating = rotationTime(intAlpha);
                    notRotatedLast = false;

                    //System.out.println("rotateLeft, x = " + nextX + ", y = " + nextY + " xx =" + x + ", yy = " + y + " rot = " + angle + "/" + intAlpha + "/" + r);
                } else if (intAlpha > 270)  {
                    intAlpha = 360-intAlpha;
                    JSONObject rotObj = new JSONObject();
                    rotObj.put("command", "right");
                    rotObj.put("args", (int)(1.05*(double)intAlpha));

                    MqttMessage rotate = new MqttMessage(rotObj.toString().getBytes());
                    mqttSender.publish("robot/process", rotate);
                    rotating = rotationTime(intAlpha);
                    notRotatedLast = false;

                    //System.out.println("rotateRight, x = " + nextX + ", y = " + nextY + " xx =" + x + ", yy = " + y + " rot = " + angle + "/" + intAlpha + "/" + r);

                } else if (intAlpha > 180){
                    intAlpha = intAlpha-180;
                    JSONObject rotObj = new JSONObject();
                    rotObj.put("command", "left");
                    rotObj.put("args", (int)(1.05*(double)intAlpha));

                    MqttMessage rotate = new MqttMessage(rotObj.toString().getBytes());
                    mqttSender.publish("robot/process", rotate);
                    rotating = rotationTime(intAlpha);
                    //System.out.println("rotateRightBkwrds, x = " + nextX + ", y = " + nextY + " xx =" + x + ", yy = " + y + " rot = " + angle + "/" + intAlpha + "/" + r);
                    notRotatedLast = false;

                } else {
                    intAlpha = Math.floorMod(180 - intAlpha,360);
                    JSONObject rotObj = new JSONObject();
                    rotObj.put("command", "right");
                    rotObj.put("args", (int)(1.05*(double)intAlpha));

                    MqttMessage rotate = new MqttMessage(rotObj.toString().getBytes());
                    mqttSender.publish("robot/process", rotate);
                    rotating = rotationTime(intAlpha);
                    //System.out.println("rotateLeftBkwrds, x = " + nextX + ", y = " + nextY + " xx =" + x + ", yy = " + y + " rot = " + angle + "/" + intAlpha + "/" + r);

                    notRotatedLast = false;
                }
            } else if (intAlpha > 270  || intAlpha < 90){
                driveForward = true;

                CurrentX = x;
                CurrentY = y;
                JSONObject obj = new JSONObject();
                obj.put("command", "forward");
                obj.put("args", 500);
                dfwd = 5;
                //System.out.println("fwd, x = " + nextX + ", y = " + nextY + " xx =" + x + ", yy = " + y);

                MqttMessage drive = new MqttMessage(obj.toString().getBytes());
                mqttSender.publish("robot/process", drive);
                notRotatedLast = true;

            } else {
                driveForward = false;

                CurrentX = x;
                CurrentY = y;
                JSONObject obj = new JSONObject();
                obj.put("command", "backward");
                obj.put("args", 500);
                dfwd = 5;

                //System.out.println("bkwrds, x = " + nextX + ", y = " + nextY + " xx =" + x + ", yy = " + y);

                MqttMessage drive = new MqttMessage(obj.toString().getBytes());
                mqttSender.publish("robot/process", drive);
                notRotatedLast = true;

            }

        } else {
            rotating--;
            dfwd--;
            //
        }
        prevRotation = r;
    }

    int rotationTime(int angle){
        return (int)(((double) angle / 360)*32) + 3;
    }
    private int prevRotation;
    private int[][] goodPoints;
    //private int[][] badPoints; // TODO
    private Boolean initialized;
    private int rotation;
    private int rotating;
    private boolean notRotatedLast;
    private int nextX;
    private int nextY;
    boolean collected,prevDriveForward;
    volatile boolean driveForward;
    private int GYRO_OFFSET;//customGyro;
    private int lastX,lastY,CurrentX,CurrentY,dfwd;

    private double myGyro(boolean df){
        int rot = (int) ((180. / Math.PI) * Math.atan2((double) (lastY - CurrentY), (double) (CurrentX - lastX)));
        if(df) {
            return Math.floorMod(rot, 360);
        } else {
            return Math.floorMod((rot + 180), 360);
        }
    }

    private double realGyro(){
        return rotation + GYRO_OFFSET;
    }

    public void weightedGyro(boolean df){
        if (lastX != 0 || lastY!= 0) {
            double CONST = 50;
            double absmoved = Math.sqrt((double) ((lastX - CurrentX) * (lastX - CurrentX) + (lastY - CurrentY) * (lastY - CurrentY)));
            double result = 100;
            if (absmoved > CONST) {
                result = myGyro(df);
                GYRO_OFFSET = (int) result - rotation;
            } else if(absmoved < 25) {
                result = realGyro();

            } else {
                result = (absmoved / CONST) * myGyro(df) + (1 - ((absmoved) / CONST)) * realGyro();
                GYRO_OFFSET = (int) result - rotation;
            }
            //customGyro = (int) myGyro();
            //return result;
        }
    }
}
