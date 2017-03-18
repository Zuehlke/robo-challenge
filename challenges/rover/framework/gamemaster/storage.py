
import pickle
import json

from gamemaster import *


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

    def load_tournament(self):
        #try:
        with open(self.filename, 'r') as file:
            jsonString = json.load(file)
            tournament = Tournament()
            tournament.players = jsonString["players"]
            tournament.played_games = [PlayedGame(g["player"], g["points"]) for g in jsonString["played_games"]]
            return tournament
        #except:
        #    return None


class TournamentEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tournament):
            played_games = [{'player': g.player, 'points': g.points} for g in obj.played_games]
            return {'players': obj.players, 'played_games': played_games }
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)
