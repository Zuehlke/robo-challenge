package main;

import main.network.Client;

public class Main {

    //private static final String BROKER = "tcp://127.0.0.1:1883";
    private static final String BROKER = "tcp://10.10.10.30:1883";

    public static void main(String[] args) {
        Client client = new Client(BROKER);
        Game game = new Game(client);
        game.start();
    }
}
