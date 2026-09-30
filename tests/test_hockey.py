import unittest

from src.hockey import (teams, to_int, clean, season, total_ot_losses,
                        worst_diff, winning_teams, teams_named)

EMPTY = "\n                            \n                        "


class TestToInt(unittest.TestCase):
    def test_whitespace_around_number(self):
        self.assertEqual(to_int("\n                            44\n                        "), 44)

    def test_negative_stays_negative(self):
        self.assertEqual(to_int("\n                            -118\n                        "), -118,
                         "pulling out just the digits drops the minus sign")

    def test_zero(self):
        self.assertEqual(to_int(" 0 "), 0)

    def test_empty_cell_is_zero(self):
        self.assertEqual(to_int(EMPTY), 0, "an empty cell is only whitespace; int('') crashes")

    def test_returns_int(self):
        self.assertIsInstance(to_int(" 44 "), int)


class TestClean(unittest.TestCase):
    def test_first_row(self):
        self.assertEqual(clean(teams)[0],
                         {"name": "Boston Bruins", "year": 1990, "wins": 44, "losses": 24, "ot_losses": 0,
                          "pct": 0.55, "gf": 299, "ga": 264, "diff": 35})

    def test_row_with_ot_losses(self):
        self.assertEqual(clean(teams)[8],
                         {"name": "St. Louis Blues", "year": 2011, "wins": 49, "losses": 22, "ot_losses": 11,
                          "pct": 0.598, "gf": 210, "ga": 165, "diff": 45})

    def test_negative_diff(self):
        self.assertEqual(clean(teams)[6]["diff"], -118)

    def test_length_and_originals_untouched(self):
        rows = clean(teams)
        self.assertEqual(len(rows), 13)
        self.assertEqual(teams[0]["wins"], "\n                            44\n                        ",
                         "the original list should be untouched")

    def test_every_name(self):
        self.assertEqual([team["name"] for team in clean(teams)],
                         ["Boston Bruins", "Chicago Blackhawks", "Detroit Red Wings", "Edmonton Oilers",
                          "New York Islanders", "New York Rangers", "Quebec Nordiques", "St. Louis Blues",
                          "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs", "Vancouver Canucks",
                          "Winnipeg Jets"],
                         "every team name should be kept, stripped of the whitespace around it")

    def test_every_team(self):
        self.assertEqual(clean(teams), [
            {"name": "Boston Bruins", "year": 1990, "wins": 44, "losses": 24, "ot_losses": 0, "pct": 0.55, "gf": 299, "ga": 264, "diff": 35},
            {"name": "Chicago Blackhawks", "year": 1990, "wins": 49, "losses": 23, "ot_losses": 0, "pct": 0.613, "gf": 284, "ga": 211, "diff": 73},
            {"name": "Detroit Red Wings", "year": 1990, "wins": 34, "losses": 38, "ot_losses": 0, "pct": 0.425, "gf": 273, "ga": 298, "diff": -25},
            {"name": "Edmonton Oilers", "year": 1990, "wins": 37, "losses": 37, "ot_losses": 0, "pct": 0.463, "gf": 272, "ga": 272, "diff": 0},
            {"name": "New York Islanders", "year": 1990, "wins": 25, "losses": 45, "ot_losses": 0, "pct": 0.312, "gf": 223, "ga": 290, "diff": -67},
            {"name": "New York Rangers", "year": 1990, "wins": 36, "losses": 31, "ot_losses": 0, "pct": 0.45, "gf": 297, "ga": 265, "diff": 32},
            {"name": "Quebec Nordiques", "year": 1990, "wins": 16, "losses": 50, "ot_losses": 0, "pct": 0.2, "gf": 236, "ga": 354, "diff": -118},
            {"name": "St. Louis Blues", "year": 1990, "wins": 47, "losses": 22, "ot_losses": 0, "pct": 0.588, "gf": 310, "ga": 250, "diff": 60},
            {"name": "St. Louis Blues", "year": 2011, "wins": 49, "losses": 22, "ot_losses": 11, "pct": 0.598, "gf": 210, "ga": 165, "diff": 45},
            {"name": "Tampa Bay Lightning", "year": 2011, "wins": 38, "losses": 36, "ot_losses": 8, "pct": 0.463, "gf": 235, "ga": 281, "diff": -46},
            {"name": "Toronto Maple Leafs", "year": 2011, "wins": 35, "losses": 37, "ot_losses": 10, "pct": 0.427, "gf": 231, "ga": 264, "diff": -33},
            {"name": "Vancouver Canucks", "year": 2011, "wins": 51, "losses": 22, "ot_losses": 9, "pct": 0.622, "gf": 249, "ga": 198, "diff": 51},
            {"name": "Winnipeg Jets", "year": 2011, "wins": 37, "losses": 35, "ot_losses": 10, "pct": 0.451, "gf": 225, "ga": 246, "diff": -21},
        ])


class TestQuestions(unittest.TestCase):
    def setUp(self):
        self.rows = clean(teams)

    def test_season(self):
        self.assertEqual(len(season(self.rows, 1990)), 8)
        self.assertEqual([r["name"] for r in season(self.rows, 2011)][:2], ["St. Louis Blues", "Tampa Bay Lightning"])
        self.assertEqual(season(self.rows, 1995), [])

    def test_total_ot_losses(self):
        self.assertEqual(total_ot_losses(self.rows, 2011), 48)
        self.assertEqual(total_ot_losses(self.rows, 1990), 0, "1990 had no overtime-loss column filled in")

    def test_worst_diff(self):
        self.assertEqual(worst_diff(self.rows), -118)

    def test_winning_teams(self):
        self.assertEqual(winning_teams(self.rows, 1990), ["Boston Bruins", "Chicago Blackhawks", "St. Louis Blues"])
        self.assertEqual(winning_teams(self.rows, 2011), ["St. Louis Blues", "Vancouver Canucks"])

    def test_teams_named(self):
        self.assertEqual(teams_named(self.rows, "new york"), ["New York Islanders (1990)", "New York Rangers (1990)"])

    def test_teams_named_any_case_and_both_years(self):
        self.assertEqual(teams_named(self.rows, "ST. LOUIS"), ["St. Louis Blues (1990)", "St. Louis Blues (2011)"])

    def test_teams_named_none(self):
        self.assertEqual(teams_named(self.rows, "kings"), [])


if __name__ == "__main__":
    unittest.main()
