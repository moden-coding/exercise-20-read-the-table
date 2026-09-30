import re

# What a scraper collected from the hockey table at scrapethissite.com/pages/forms:
# one dictionary per row, every cell still the raw text from the page. Nothing has been cleaned yet.
# (These are real rows from the 1990 and 2011 seasons.)
teams = [
    {"name": '\n                            Boston Bruins\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            44\n                        ', "losses": '\n                            24\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.55\n                        ', "gf": '\n                            299\n                        ', "ga": '\n                            264\n                        ', "diff": '\n                            35\n                        '},
    {"name": '\n                            Chicago Blackhawks\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            49\n                        ', "losses": '\n                            23\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.613\n                        ', "gf": '\n                            284\n                        ', "ga": '\n                            211\n                        ', "diff": '\n                            73\n                        '},
    {"name": '\n                            Detroit Red Wings\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            34\n                        ', "losses": '\n                            38\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.425\n                        ', "gf": '\n                            273\n                        ', "ga": '\n                            298\n                        ', "diff": '\n                            -25\n                        '},
    {"name": '\n                            Edmonton Oilers\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            37\n                        ', "losses": '\n                            37\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.463\n                        ', "gf": '\n                            272\n                        ', "ga": '\n                            272\n                        ', "diff": '\n                            0\n                        '},
    {"name": '\n                            New York Islanders\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            25\n                        ', "losses": '\n                            45\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.312\n                        ', "gf": '\n                            223\n                        ', "ga": '\n                            290\n                        ', "diff": '\n                            -67\n                        '},
    {"name": '\n                            New York Rangers\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            36\n                        ', "losses": '\n                            31\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.45\n                        ', "gf": '\n                            297\n                        ', "ga": '\n                            265\n                        ', "diff": '\n                            32\n                        '},
    {"name": '\n                            Quebec Nordiques\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            16\n                        ', "losses": '\n                            50\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.2\n                        ', "gf": '\n                            236\n                        ', "ga": '\n                            354\n                        ', "diff": '\n                            -118\n                        '},
    {"name": '\n                            St. Louis Blues\n                        ', "year": '\n                            1990\n                        ', "wins": '\n                            47\n                        ', "losses": '\n                            22\n                        ', "ot_losses": '\n                            \n                        ', "pct": '\n                            0.588\n                        ', "gf": '\n                            310\n                        ', "ga": '\n                            250\n                        ', "diff": '\n                            60\n                        '},
    {"name": '\n                            St. Louis Blues\n                        ', "year": '\n                            2011\n                        ', "wins": '\n                            49\n                        ', "losses": '\n                            22\n                        ', "ot_losses": '\n                            11\n                        ', "pct": '\n                            0.598\n                        ', "gf": '\n                            210\n                        ', "ga": '\n                            165\n                        ', "diff": '\n                            45\n                        '},
    {"name": '\n                            Tampa Bay Lightning\n                        ', "year": '\n                            2011\n                        ', "wins": '\n                            38\n                        ', "losses": '\n                            36\n                        ', "ot_losses": '\n                            8\n                        ', "pct": '\n                            0.463\n                        ', "gf": '\n                            235\n                        ', "ga": '\n                            281\n                        ', "diff": '\n                            -46\n                        '},
    {"name": '\n                            Toronto Maple Leafs\n                        ', "year": '\n                            2011\n                        ', "wins": '\n                            35\n                        ', "losses": '\n                            37\n                        ', "ot_losses": '\n                            10\n                        ', "pct": '\n                            0.427\n                        ', "gf": '\n                            231\n                        ', "ga": '\n                            264\n                        ', "diff": '\n                            -33\n                        '},
    {"name": '\n                            Vancouver Canucks\n                        ', "year": '\n                            2011\n                        ', "wins": '\n                            51\n                        ', "losses": '\n                            22\n                        ', "ot_losses": '\n                            9\n                        ', "pct": '\n                            0.622\n                        ', "gf": '\n                            249\n                        ', "ga": '\n                            198\n                        ', "diff": '\n                            51\n                        '},
    {"name": '\n                            Winnipeg Jets\n                        ', "year": '\n                            2011\n                        ', "wins": '\n                            37\n                        ', "losses": '\n                            35\n                        ', "ot_losses": '\n                            10\n                        ', "pct": '\n                            0.451\n                        ', "gf": '\n                            225\n                        ', "ga": '\n                            246\n                        ', "diff": '\n                            -21\n                        '},
]


# Three made-up rows that are already clean. The examples below use them, so you can
# try the questions before clean() works.
sample = [
    {"name": "Ottawa Senators", "year": 2000, "wins": 40, "losses": 30, "ot_losses": 2,
     "pct": 0.6, "gf": 200, "ga": 180, "diff": 20},
    {"name": "Boston Bruins",   "year": 2000, "wins": 35, "losses": 35, "ot_losses": 3,
     "pct": 0.5, "gf": 190, "ga": 193, "diff": -3},
    {"name": "Ottawa Senators", "year": 2001, "wins": 30, "losses": 45, "ot_losses": 4,
     "pct": 0.4, "gf": 170, "ga": 182, "diff": -12},
]


def to_int(text):
    """The cell as an int. An empty cell (only whitespace) becomes 0. Negative numbers stay negative.

    to_int(teams[0]["wins"])       ->  44
    to_int(teams[6]["diff"])       ->  -118
    to_int(teams[0]["ot_losses"])  ->  0        (an empty cell)
    to_int("   7   ")              ->  7
    """
    pass


def clean(teams):
    """Row in, row out: a new list of dicts. "name" is a clean string, "pct" is a float, every other value is an int.

    clean(teams)[0]  ->  {'name': 'Boston Bruins', 'year': 1990, 'wins': 44, 'losses': 24, 'ot_losses': 0,
                          'pct': 0.55, 'gf': 299, 'ga': 264, 'diff': 35}
    """
    pass


def season(rows, year):
    """The rows from that year, in order.

    season(sample, 2001)  ->  [sample[2]]    (the 2001 Ottawa Senators row)
    season(sample, 1999)  ->  []
    """
    pass


def total_ot_losses(rows, year):
    """Total overtime losses across every team in that year.

    total_ot_losses(sample, 2000)  ->  5
    total_ot_losses(sample, 2001)  ->  4
    """
    pass


def worst_diff(rows):
    """The lowest goal differential ("diff") in the rows.

    worst_diff(sample)  ->  -12
    """
    pass


def winning_teams(rows, year):
    """Names of teams in that year with a win percentage above 0.5.

    winning_teams(sample, 2000)  ->  ['Ottawa Senators']    (Boston's 0.5 is not above 0.5)
    winning_teams(sample, 2001)  ->  []
    """
    pass


def teams_named(rows, word):
    """Names (with the year in parentheses, like "New York Rangers (1990)") whose name mentions the word, any capitalization.

    teams_named(sample, "OTTAWA")  ->  ['Ottawa Senators (2000)', 'Ottawa Senators (2001)']
    teams_named(sample, "bruins")  ->  ['Boston Bruins (2000)']
    teams_named(sample, "kings")   ->  []
    """
    pass


def main():
    # Run `python src/hockey.py` and compare each line to the examples in the docstrings.
    print('to_int(teams[0]["wins"])       -> ', to_int(teams[0]["wins"]))
    print('to_int(teams[6]["diff"])       -> ', to_int(teams[6]["diff"]))
    print('to_int(teams[0]["ot_losses"])  -> ', to_int(teams[0]["ot_losses"]))
    print('to_int("   7   ")              -> ', to_int("   7   "))
    print('season(sample, 2001)           -> ', season(sample, 2001))
    print('season(sample, 1999)           -> ', season(sample, 1999))
    print('total_ot_losses(sample, 2000)  -> ', total_ot_losses(sample, 2000))
    print('total_ot_losses(sample, 2001)  -> ', total_ot_losses(sample, 2001))
    print('worst_diff(sample)             -> ', worst_diff(sample))
    print('winning_teams(sample, 2000)    -> ', winning_teams(sample, 2000))
    print('winning_teams(sample, 2001)    -> ', winning_teams(sample, 2001))
    print('teams_named(sample, "OTTAWA")  -> ', teams_named(sample, "OTTAWA"))
    print('teams_named(sample, "bruins")  -> ', teams_named(sample, "bruins"))
    print('teams_named(sample, "kings")   -> ', teams_named(sample, "kings"))

    rows = clean(teams)
    if rows is None:
        print("Finish clean() to see the answers for the real table.")
    else:
        print()
        print("The real table")
        print(rows[0])
        print(total_ot_losses(rows, 1990), total_ot_losses(rows, 2011))
        print(worst_diff(rows))
        print(winning_teams(rows, 2011))
        print(teams_named(rows, "new york"))


if __name__ == "__main__":
    main()
