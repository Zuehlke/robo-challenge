#!/bin/env python3

import logging
import time
import re
import json
import paho.mqtt.client as mqtt

from game import Game

GAME_LENGTH_SECONDS = 60

logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)


class CurrentGame:
    def __init__(self, player):
        self.player = player
        self.start_time = 0
        self.game = Game()

    def start(self):
        self.start_time = time.time()

    def elapsed_time(self):
        return time.time() - self.start_time

    def is_started(self):
        return self.start_time > 0

    def is_finished(self):
        return self.start_time <= (time.time() - GAME_LENGTH_SECONDS)


class PlayedGame:
    def __init__(self, player, points):
        self.player = player
        self.points = points

    def __str__(self):
        return "PlayedGame(%s,%d)" % (self.player, self.points)

    def __eq__(self, other):
        return self.player == other.player and self.points == other.points


class Rank:
    def __init__(self, player, points):
        self.player = player
        self.points = points

    def __str__(self):
        return "Rank(%s,%d)" % (self.player, self.points)

    def __eq__(self, other):
        return self.player == other.player and self.points == other.points


class Tournament:
    def __init__(self):
        self.players = []
        self.played_games = []
        self.current_game = None

    def register_player(self, name):
        if name in self.players:
            return

        self.players.append(name)

    def store_played_game(self, played_game):
        if played_game.player not in self.players:
            return

        self.played_games.append(played_game)

    def prepare_game(self, player):
        if player not in self.players:
            logging.warning("Attempting to prepare game for unknown player: %s" % player)
            return

        self.current_game = CurrentGame(player)

    def start_game(self):
        if self.current_game is None:
            logging.warning("Attempting to start unprepared game")
            return

        self.current_game.start()

    def finish_game(self):
        if self.current_game is None:
            logging.warning("Attempting to finish not started game")
            return

        self.played_games.append(PlayedGame(self.current_game.player, self.current_game.game.score()))
        self.current_game = None

    def leaderboard(self):
        board = []

        for player in self.players:
            games_of_player = [game.points for game in self.played_games if game.player == player]
            points = max(games_of_player) if len(games_of_player) > 0 else 0
            board.append(Rank(player, points))

        return sorted(board, key=lambda game: game.points, reverse=True)

from common import CommandDispatcher


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
        self.dispatcher = CommandDispatcher(self)
        return self

    def __exit__(self, type, value, traceback):
        self.client.disconnect()

    def process_messages(self, timeout=1.0):
        self.client.loop(timeout)

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
            result = re.search("(?:players/)(\w+)", msg.topic)
            if result is not None:
                player = result.group(1)
                logging.info("Registering player: " + player)
                self.tournament.register_player(player)
            else:
                obj = json.loads(msg.payload.decode('utf-8'))
                self.dispatcher.exec(obj)

        except Exception as ex:
            logging.exception("Error processing message")

    def prepare(self, player):
        logging.info("Preparing game for player %s" % player)
        self.tournament.prepare_game(player)
        self.client.publish("players/"+player, json.dumps({'command': 'start'}))

    def start(self):
        logging.info("Starting game")
        self.tournament.start_game()
