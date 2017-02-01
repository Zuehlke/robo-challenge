#!/bin/env python3

import time
import re
import json
import logging
import paho.mqtt.client as mqtt

from gamemaster import Tournament
from common import TopicAwareCommandDispatcher

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class TournamentRadio:
    def __init__(self, host, port, tournament):
        self.host = host
        self.port = port
        self.tournament = tournament

    def __enter__(self):
        self.client = mqtt.Client("Game Master")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        self.dispatcher = TopicAwareCommandDispatcher(self)
        return self

    def __exit__(self, type, value, traceback):
        self.client.disconnect()

    def game_loop(self, timeout=1.0):
        self.client.loop(timeout)
        if self.tournament.current_game is not None and self.tournament.current_game.is_started():
            if self.tournament.current_game.is_finished():
                player = self.tournament.current_game.player
                logging.info("Game for player %s finished" % player)
                self.tournament.finish_game()
                self.client.publish("players/"+player, json.dumps({'command': 'finished'}))

    def publish_tournament(self, tournament):
        payload = json.dumps({
            'currentGame': self.current_game_state(tournament),
            'leaderboard': [{'player': r.player, 'points': r.points} for r in tournament.leaderboard()]
        })
        self.client.publish("tournament", payload)

    def current_game_state(self, tournament):
        if tournament.current_game is None:
            return {'player': '', 'state': 'OPEN', 'time': 0}

        return {
            'player': tournament.current_game.player,
            'state': 'RUNNING' if tournament.current_game.is_started() else 'READY',
            'time': tournament.current_game.elapsed_time() if tournament.current_game.is_started() else 0
        }

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code "+str(rc))

        self.client.subscribe("players/+")
        self.client.subscribe("gamemaster")

    def on_message(self, client, userdata, msg):
        logging.info("Received message '" + str(msg.payload) + " on topic " + msg.topic + " with QoS " + str(msg.qos))

        try:
            obj = json.loads(msg.payload.decode('utf-8'))
            self.dispatcher.exec(msg.topic, obj)

        except Exception as ex:
            logging.exception("Error processing message")

    def extract_player_from_topic(self, topic):
        result = re.search("(?:players/)(\w+)", topic)
        if result is not None:
            player = result.group(1)

            return player
        else:
            return None

    def register(self, topic):
        player = self.extract_player_from_topic(topic)
        logging.info("Registering player: " + player)
        self.tournament.register_player(player)

    def prepare(self, topic, player):
        logging.info("Preparing game for player %s" % player)
        self.tournament.prepare_game(player)
        self.client.publish("players/"+player, json.dumps({'command': 'start'}))

    def start(self, topic):
        player = self.extract_player_from_topic(topic)
        if self.tournament.current_game.player != player:
            logging.warning("%s attempted to start game for other player %s" % (player, self.tournament.current_game.player))
            return

        logging.info("Starting game for player %s" % player)
        self.tournament.start_game()


LOOP_CYCLE_TIME_SEC = 0.5

if __name__ == '__main__':
    tournament = Tournament()

    with TournamentRadio("broker", 1883, tournament) as radio:
        while True:
            radio.game_loop(LOOP_CYCLE_TIME_SEC)
            radio.publish_tournament(tournament)
            time.sleep(1)
