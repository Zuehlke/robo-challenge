#!/bin/env python3

import logging
import time

from game import Game

GAME_LENGTH_SECONDS = 60


class CurrentGame:
    def __init__(self, player):
        self.player = player
        self.start_time = 0
        self.robot_position = {'x': 0, 'y': 0, 'r': 0}
        self.game = Game()

    def start(self):
        self.start_time = time.time()

    def update_robot_position(self, robot_position):
        self.robot_position = robot_position
        self.game.check(robot_position.x, robot_position.y, robot_position.r)

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
