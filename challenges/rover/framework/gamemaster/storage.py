
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

    def load_tournament(self, points=None):
        try:
            with open(self.filename, 'r') as file:
                jsonString = json.load(file)
                tournament = Tournament(points)
                tournament.players = jsonString["players"]
                tournament.played_games = [PlayedGame(g["player"], g["points"]) for g in jsonString["played_games"]]
                return tournament
        except:
            return None

class JsonPointsStorage:
    def __init__(self, filename="points.json"):
        self.filename = file

    def store_points(self, points):
        with open(self.filename, 'w') as file:
            json.dump({'points': points}, file, cls=PointsEncoder)

    def load_points(self):
        try:
            with open(self.filename, 'r') as file:
                jsonString = json.load(file)
                points = [Point(g["x"], g["y"], g["r"]) for g in jsonString["points"]]
                return points
        except:
            return None

class TournamentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tournament):
            played_games = [{'player': g.player, 'points': g.points} for g in obj.played_games]
            return {'players': obj.players, 'played_games': played_games }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class PointsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, dict):
            points = [{'x': g.x, 'y': g.y, 'r': g.r} for g in obj.points]
            return {'points': points }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
