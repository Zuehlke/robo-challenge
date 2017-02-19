import org.eclipse.paho.client.mqttv3.*;
import org.json.*;
import java.util.UUID;

public class Client implements MqttCallback{

    private static final String PLAYER_NAME  = "foo";


    private static final String BROKER = "tcp://127.0.0.1:1883";

    private MqttClient client;

    private Client(MqttClient client) {
        this.client = client;
    }

    public static void main(String[] args) {

        try {
            MqttClient mqtt = new MqttClient(BROKER, UUID.randomUUID().toString());
            MqttConnectOptions connOpts = new MqttConnectOptions();
            mqtt.connect(connOpts);

            System.out.println("Connecting to broker: " + BROKER);

            mqtt.setCallback(new Client(mqtt));

            mqtt.subscribe("players/" + PLAYER_NAME + "/#");
            mqtt.subscribe("robot/state");


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
        System.out.println(topic);
        JSONObject obj = new JSONObject(new String(mqttMessage.getPayload()));
        System.out.println(obj);

        // TODO: implement algorithm
    }

    @Override
    public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {

    }
}

