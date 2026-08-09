import csv
import os


def get_stats(path="sessions.csv"):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    nb_sessions = 0
    total_time_played = 0
    total_profit = 0
    profits = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            nb_sessions += 1
            total_time_played += int(row["duration_seconds"])
            profit = int(row["profit"])
            total_profit += profit
            profits.append(profit)

    if nb_sessions > 0:
        avg_profit_per_session = total_profit / nb_sessions
        best_session_profit = max(profits)
        worst_session_profit = min(profits)
    else:
        avg_profit_per_session = 0
        best_session_profit = 0
        worst_session_profit = 0

    return {
        "nb_sessions": nb_sessions,
        "total_time_played": total_time_played,
        "total_profit": total_profit,
        "avg_profit_per_session": avg_profit_per_session,
        "best_session_profit": best_session_profit,
        "worst_session_profit": worst_session_profit,
        "profits": profits,
    }

        