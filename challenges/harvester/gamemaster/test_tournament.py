
import unittest
from gamemaster import Tournament, PlayedGame, Rank


class TournamentTests(unittest.TestCase):

    def test_init(self):
        tournament = Tournament()

        self.assertEqual(tournament.players, [])
        self.assertEqual(tournament.played_games, [])
        self.assertEqual(tournament.leaderboard(), [])

    def test_register_player(self):
        tournament = Tournament()

        tournament.register_player("player1")

        self.assertEqual(tournament.players, ["player1"])

    def test_store_played_game_unknown_player(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.store_played_game(PlayedGame("player2", 17))

        self.assertEqual(tournament.played_games, [])

    def test_store_played_game_known_player(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.store_played_game(PlayedGame("player1", 17))

        self.assertEqual(tournament.played_games, [PlayedGame("player1", 17)])

    def test_leaderboard_no_games_played(self):
        tournament = Tournament()

        tournament.register_player("player1")

        self.assertEqual(tournament.leaderboard(), [Rank("player1", 0)])

    def test_leaderboard_games_played(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.register_player("player2")
        tournament.store_played_game(PlayedGame("player1", 17))
        tournament.store_played_game(PlayedGame("player2", 15))
        tournament.store_played_game(PlayedGame("player1", 3))

        self.assertEqual(tournament.leaderboard(), [Rank("player1", 20), Rank("player2", 15)])
