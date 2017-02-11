
import unittest
from gamemaster import Tournament, PlayedGame, Rank


class TournamentTests(unittest.TestCase):

    def test_init(self):
        tournament = Tournament()

        self.assertEqual(tournament.players, [])
        self.assertEqual(tournament.played_games, [])
        self.assertEqual(tournament.leaderboard(), [])
        self.assertEqual(tournament.current_game, None)

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

        self.assertEqual(tournament.leaderboard(), [Rank("player1", 17), Rank("player2", 15)])

    def test_leaderboard_games_played_ordered_by_points(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.register_player("player2")
        tournament.store_played_game(PlayedGame("player1", 15))
        tournament.store_played_game(PlayedGame("player2", 18))

        self.assertEqual(tournament.leaderboard(), [Rank("player2", 18), Rank("player1", 15)])

    def test_prepare_game_unknown_player(self):
        tournament = Tournament()

        tournament.prepare_game("player1")

        self.assertEqual(tournament.current_game, None)

    def test_prepare_game_known_player(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.prepare_game("player1")

        self.assertEqual(tournament.current_game.player, "player1")
        self.assertIsNotNone(tournament.current_game.start_time)

    def test_start_game_prepared_game(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.prepare_game("player1")
        tournament.start_game()

        self.assertTrue(tournament.current_game.start_time > 0)

    def test_start_game_no_prepared_game(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.start_game()

        self.assertEqual(tournament.current_game, None)

    def test_is_finished(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.prepare_game("player1")
        tournament.start_game()

        self.assertFalse(tournament.current_game.is_finished())

    def test_update_robot_state(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.prepare_game("player1")
        tournament.start_game()

        first_point = tournament.current_game.game.points()[0]

        tournament.update_robot_position({'x': first_point.x, 'y': first_point.y, 'r': 5})
        tournament.finish_game()

        self.assertIsNone(tournament.current_game)
        self.assertEqual(tournament.played_games, [PlayedGame("player1", 1)])

    def test_is_finished_time_elapsed(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.prepare_game("player1")
        tournament.start_game()
        tournament.current_game.start_time = 0

        self.assertTrue(tournament.current_game.is_finished())

    def test_finish(self):
        tournament = Tournament()

        tournament.register_player("player1")
        tournament.prepare_game("player1")
        tournament.start_game()
        tournament.finish_game()

        self.assertIsNone(tournament.current_game)
        self.assertEqual(tournament.played_games, [PlayedGame("player1", 0)])
