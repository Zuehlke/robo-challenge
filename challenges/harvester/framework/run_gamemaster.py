#!/bin/env python3

import time
import re
import json
import logging
import paho.mqtt.client as mqtt

from game import Point
from gamemaster import Tournament, PickleTournamentStorage
from common import TopicAwareCommandDispatcher

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class PointEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Point):
            return {'x': obj.x, 'y': obj.y, 'r': obj.r, 'score': obj.score, 'collected': obj.collected}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class TournamentRadio:
    def __init__(self, host, port, tournament, storage):
        self.host = host
        self.port = port
        self.tournament = tournament
        self.storage = storage

    def __enter__(self):
        self.client = mqtt.Client("Game Master")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        self.dispatcher = TopicAwareCommandDispatcher(self)
        return self

    def __exit__(self, type, value, traceback):
        self.client.disconnect()

    def is_game_started(self):
        return self.tournament.current_game is not None and self.tournament.current_game.is_started()

    def game_loop(self, timeout=1.0):
        self.client.loop(timeout)
        if self.is_game_started():
            if self.tournament.current_game.is_finished():
                player = self.tournament.current_game.player
                logging.info("Game for player %s finished" % player)
                self.tournament.finish_game()
                self.storage.store_tournament(self.tournament)
                self.client.publish(self.response_topic_for_player(player), json.dumps({'command': 'finished'}))

    def publish_tournament(self):
        payload = json.dumps({
            'currentGame': self.current_game_state(),
            'leaderboard': [{'player': r.player, 'points': r.points} for r in self.tournament.leaderboard()]
        })
        self.client.publish("tournament", payload)
        if self.is_game_started():
            player = self.tournament.current_game.player
            game = json.dumps(self.current_game_details(), cls=PointEncoder)
            self.client.publish("players/"+player+"/game", game)
            self.client.publish("game/state", game)

    def current_game_details(self):
        current_game = self.tournament.current_game
        return {'robot': {
                    'x': current_game.robot_position['x'],
                    'y': current_game.robot_position['y'],
                    'r': current_game.robot_position['r']
                    },
                'world': {'x_max': current_game.game.max_x(), 'y_max': current_game.game.max_y()},
                'points': current_game.game.points()
                }

    def current_game_state(self):
        if self.tournament.current_game is None:
            return {'player': '', 'state': 'OPEN', 'time': 0}

        return {
            'player': self.tournament.current_game.player,
            'state': 'RUNNING' if self.tournament.current_game.is_started() else 'READY',
            'time': self.tournament.current_game.elapsed_time() if self.tournament.current_game.is_started() else 0
        }

    def on_connect(self, client, userdata, flags, rc):
        logging.info("Connected with result code "+str(rc))

        self.client.subscribe("players/+")
        self.client.subscribe("gamemaster")
        self.client.subscribe("robot/position")

    def on_message(self, client, userdata, msg):
        logging.debug("Received message '" + str(msg.payload) + " on topic " + msg.topic + " with QoS " + str(msg.qos))

        try:
            obj = json.loads(msg.payload.decode('utf-8'))
            if msg.topic == "robot/position":
                self.tournament.update_robot_position(obj)
            else:
                # Command dispatch
                self.dispatcher.exec(msg.topic, obj)

        except Exception as ex:
            logging.exception("Error processing message")

    def response_topic_for_player(self, player):
        return "players/%s/incoming" % player

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
        self.client.publish(self.response_topic_for_player(player), json.dumps({'command': 'start'}))

    def start(self, topic):
        player = self.extract_player_from_topic(topic)
        if self.tournament.current_game is not None and self.tournament.current_game.player != player:
            logging.warning("%s attempted to start game for other player %s" % (player, self.tournament.current_game.player))
            return

        logging.info("Starting game for player %s" % player)
        self.tournament.start_game()

LOOP_TIMEOUT = 0.1
LOOP_CYCLE_TIME_SEC = 0.5

if __name__ == '__main__':
    storage = PickleTournamentStorage("/framework/tournament.pickle")
    tournament = storage.load_tournament() or Tournament()

    with TournamentRadio("broker", 1883, tournament, storage) as radio:
        while True:
            radio.game_loop(LOOP_CYCLE_TIME_SEC)
            radio.publish_tournament()
            time.sleep(LOOP_TIMEOUT)
