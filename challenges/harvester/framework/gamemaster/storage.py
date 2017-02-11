
import pickle


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
