#!/bin/env python3

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

    def register_player(self, name):
        if name in self.players:
            return

        self.players.append(name)

    def store_played_game(self, played_game):
        if played_game.player not in self.players:
            return

        self.played_games.append(played_game)

    def leaderboard(self):
        board = []

        for player in self.players:
            board.append(Rank(player, sum([game.points for game in self.played_games if game.player == player])))

        return board


import paho.mqtt.client as mqtt
import json

class TournamentRadio:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __enter__(self):
        self.client = mqtt.Client("Game Master")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.host, self.port, 60)
        return self

    def __exit__(self, type, value, traceback):
        self.client.disconnect()

    def process_messages(self, timeout=1.0):
        self.client.loop(timeout)

    def publish_tournament(self, tournament):
        payload = json.dumps({'leaderboard': [{'player': r.player, 'points': r.points} for r in tournament.leaderboard()]})
        self.client.publish("tournament", payload)

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

import time

LOOP_CYCLE_TIME_SEC=0.5

if __name__ == '__main__':
    tournament = Tournament()

    with TournamentRadio("broker", 1883) as radio:
        while True:
            radio.process_messages(LOOP_CYCLE_TIME_SEC)
            radio.publish_tournament(tournament)
            time.sleep(0.01)
