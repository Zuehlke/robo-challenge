package main;

import main.control.Controller;
import main.graph.*;
import main.network.Client;
import main.pathfinder.PathFinder;

public class Game implements Client.ClientListener {

    private Client mClient;
    private Controller mController;

    public Game(Client client) {
        mClient = client;
        mClient.setClientListener(this);

        mController = new Controller(client);
    }

    public void start() {
        mClient.register();
    }

    @Override
    public void receivedStartMessage() {
        mClient.start();
    }

    @Override
    public void receivedTopology(Topology topology, Point startPosition) {
        //PathFinder finder = new PathFinder(topology, startPosition);
        //Path path = finder.computePath(40);

        TokenQueue queue = new TokenQueue(topology.getTokens());
        mController.setTokens(queue, startPosition);
        mController.start();
    }
}
