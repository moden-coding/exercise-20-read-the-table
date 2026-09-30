# Exercise 20: Read the table

A scraper visited a page with a table of NHL team records and saved every row in `src/hockey.py` as a list
called `teams`: one dictionary per row, every cell still the **raw text** from the page. These are real
rows from the 1990 and 2011 seasons.

```python
{"name": "\n                            Boston Bruins\n                        ",
 "wins": "\n                            44\n                        ",
 "ot_losses": "\n                            \n                        ", ...}
```

Every cell comes wrapped in the line breaks and spaces the page used to indent its HTML. Clean the rows,
then answer four questions. Write these functions in `src/hockey.py`.

**Cleaning**

1. `to_int(text)` — the cell as an **int**. An empty cell (nothing but whitespace) becomes `0`. Negative numbers stay negative.
2. `clean(teams)` — row in, row out: a **new** list of dictionaries with the same keys. `"name"` is a clean string, `"pct"` is a float, and every other value is an int. Single `return`.

**Questions** (each takes the output of `clean`)

3. `season(rows, year)` — the rows from that year, in order.
4. `total_ot_losses(rows, year)` — total overtime losses across every team that year.
5. `worst_diff(rows)` — the lowest goal differential (`"diff"`) anywhere in the rows.
6. `winning_teams(rows, year)` — names of teams that year with a win percentage **above** 0.5.
7. `teams_named(rows, word)` — every team whose name mentions `word` in any capitalization, written as `"Name (year)"`.

```
rows = clean(teams)
rows[0]                         ->  {'name': 'Boston Bruins', 'year': 1990, 'wins': 44, 'losses': 24, 'ot_losses': 0, 'pct': 0.55, 'gf': 299, 'ga': 264, 'diff': 35}
total_ot_losses(rows, 2011)     ->  48
worst_diff(rows)                ->  -118
winning_teams(rows, 2011)       ->  ['St. Louis Blues', 'Vancouver Canucks']
teams_named(rows, "new york")   ->  ['New York Islanders (1990)', 'New York Rangers (1990)']
```

## Tools you'll need

- `.strip()`, `int()`, and `float()` from Chapter 3.
- The `x if condition else y` form, for the empty cells.
- `re.search(word, text, re.IGNORECASE)` as a filter condition, only for `teams_named`.

## Watch for

- **Most of this needs no regex.** Once a cell is stripped it's already a clean number. Reach for regex when the text has junk mixed in, not by habit.
- The goal differential for one team is `-118`. Pulling the digits out with `re.findall` gives `118` and quietly drops the minus sign. Three tests check for this.
- In 1990 the overtime-loss cells are empty: only whitespace. `int("")` crashes.
- The St. Louis Blues appear twice, once per season. That's why `teams_named` includes the year.

## Running the tests

From the top folder of this repo:

```
python -m unittest discover
```

Run `python src/hockey.py` from the top folder after each function you write. It runs the examples from
each docstring, so you can compare what prints to what the docstring says before running the tests.

**Where this list came from:** these are the actual cells a scraper gets from the hockey table at
scrapethissite.com, whitespace and all. Next unit you'll write that scraper yourself, and your `clean`
function will be waiting for its output.
