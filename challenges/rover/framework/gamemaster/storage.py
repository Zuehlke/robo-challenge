
import pickle
import json

from gamemaster import *
from game import Point


class PickleTournamentStorage:
    def __init__(self, file="tournament.pickle"):
        self.filename = file

    def store_tournament(self, tournament):
        with open(self.filename, 'wb') as file:
            pickle.dump(tournament, file)

    def load_tournament(self):
        try:
            with open(self.filename, 'rb') as file:
                return pickle.load(file)
        except:
            return None

class JsonTournamentStorage:
    def __init__(self, file="tournament.json"):
        self.filename = file

    def store_tournament(self, tournament):
        with open(self.filename, 'w') as file:
            json.dump(tournament, file, cls=TournamentEncoder)

    def load_tournament(self, game_creator=None):
        try:
            with open(self.filename, 'r') as file:
                jsonString = json.load(file)
                tournament = Tournament(game_creator)
                tournament.players = jsonString["players"]
                tournament.played_games = [PlayedGame(g["player"], g["points"]) for g in jsonString["played_games"]]
                return tournament
        except:
            return None

class JsonGameStorage:
    def __init__(self, filename="game.json"):
        self.filename = file

    def store_game(self, game):
        with open(self.filename, 'w') as file:
            json.dump(game, file, cls=GameEncoder)

    def load_game(self):
        try:
            with open(self.filename, 'r') as file:
                jsonString = json.load(file)
                points = [Point(g["x"], g["y"], g["r"], g["collected"], g["score"]) for g in jsonString["points"]]
                points_creator = StoredPointsCreator(points)
                game = Game(max_x=jsonString["max_x"], max_y=jsonString["max_y"], radius=jsonString["radius"], distance=jsonString["distance"], pointsCreator=points_creator)
                return game
        except:
            return None

class TournamentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tournament):
            played_games = [{'player': g.player, 'points': g.points} for g in obj.played_games]
            return {'players': obj.players, 'played_games': played_games }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class StoredPointsCreator:
    def __init__(self, points):
        self.__points = points

    def create_points(self, max_x, max_y):
        return self.__points

class GameEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Game):
            points = [{'x': g.x, 'y': g.y, 'r': g.r, 'collected': g.collected, 'score': g.score} for g in obj.points()]
            return {'max_x': obj.max_x(), 'max_y': obj.max_y(), 'radius': obj.radius(), 'distance': obj.distance(), 'points': points }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
