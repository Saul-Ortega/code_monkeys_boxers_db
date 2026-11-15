"""FACUNDO: show the best and worst boxers from the existing boxers.db.

Run after the shared notebook has created and populated the database:
    python best_and_worst_boxer.py

To use points, import the function and call it with metric="points".
"""

from contextlib import closing
import sqlite3

import pandas as pd


def show_best_and_worst_boxer(metric: str = "win_rate") -> None:
  """
  Find and print the best and worst boxers from the database.

  Boxers with no fights are excluded. If several boxers share the
  highest or lowest score, all of them are shown.

  Args:
    metric (str, optional): "win_rate" calculates wins / total_fights
      as a percentage. "points" assigns 3 points per win and 1 per draw.
      Defaults to "win_rate".

  Returns:
    None
  """
  if metric not in ("win_rate", "points"):
    print('Error: Choose "win_rate" or "points".')
    return

  try:
    with closing(sqlite3.connect("file:boxers.db?mode=ro", uri=True)) as connection:
      boxers = pd.read_sql_query(
        "SELECT id, name, total_fights, wins, loses, draws FROM boxers",
        con=connection
      )

    if boxers.empty:
      print("There are no boxers in the database.")
      return

    boxers = boxers[boxers["total_fights"] > 0].copy()

    if boxers.empty:
      print("There are no boxers with fights to compare.")
      return

    if metric == "win_rate":
      boxers["score"] = boxers["wins"] / boxers["total_fights"] * 100
    else:
      boxers["score"] = boxers["wins"] * 3 + boxers["draws"]

    best_boxers = boxers[boxers["score"] == boxers["score"].max()]
    worst_boxers = boxers[boxers["score"] == boxers["score"].min()]

    print(f"Best boxer(s) by {metric}:")
    print(best_boxers.to_string(index=False, float_format="{:.2f}".format))
    print(f"\nWorst boxer(s) by {metric}:")
    print(worst_boxers.to_string(index=False, float_format="{:.2f}".format))

  except (sqlite3.Error, pd.errors.DatabaseError) as error:
    print("Error reading the database ->", error)


if __name__ == "__main__":
  show_best_and_worst_boxer()

