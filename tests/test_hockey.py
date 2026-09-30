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
