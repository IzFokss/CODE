import tkinter as tk
import subprocess
import sys
import os

from stats import get_stats


def launch_tracker():

    tracker_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tracker.py"
    )

    subprocess.Popen(
        [sys.executable, tracker_path]
    )
window = tk.Tk()

window.title("Zynga Poker Tracker")
window.geometry("800x900")
stats_frame = tk.Frame(window)
stats_frame.pack(pady=20)


stats = get_stats()


title = tk.Label(
    window,
    text="ZYNGA POKER TRACKER",
    font=("Arial", 24)
)

title.pack(pady=30)


profit = tk.Label(
    stats_frame,
    text=f"Profit total : {stats['total_profit']:,}",
    font=("Arial", 16)
)

profit.grid(row=0, column=0, padx=30, pady=15)


sessions = tk.Label(
    stats_frame,
    text=f"Sessions : {stats['nb_sessions']}",
    font=("Arial", 16)
)

sessions.grid(row=0, column=1, padx=30, pady=15)


time_played = tk.Label(
    stats_frame,
    text=f"Temps joué : {stats['total_time_played']} secondes",
    font=("Arial", 16)
)

time_played.grid(row=1, column=0, padx=30, pady=15)



avg_profit = tk.Label(
    stats_frame,
    text=f"Profit moyen par session : {stats['avg_profit_per_session']:,}",
    font=("Arial", 16)
)
avg_profit.grid(row=1, column=1, padx=30, pady=15)

best_profit = tk.Label(
    stats_frame,
    text=f"Meilleure session : {stats['best_session_profit']:,}",
    font=("Arial", 16)
)

best_profit.grid(row=2, column=0, padx=30, pady=15)

worst_profit = tk.Label(
    stats_frame,
    text=f"Pire session : {stats['worst_session_profit']:,}",
    font=("Arial", 16)
)
worst_profit.grid(row=2, column=1, padx=30, pady=15)

win_sessions = tk.Label(
    stats_frame,
    text=f"Sessions gagnantes : {len([p for p in stats['profits'] if p > 0])}",
    font=("Arial", 16)
)
win_sessions.grid(row=3, column=0, padx=30, pady=15)

loss_sessions = tk.Label(
    stats_frame,
    text=f"Sessions perdantes : {len([p for p in stats['profits'] if p < 0])}",
    font=("Arial", 16)
)
loss_sessions.grid(row=3, column=1, padx=30, pady=15)

winrate = tk.Label(
    stats_frame,
    text=f"Winrate : {len([p for p in stats['profits'] if p > 0]) / stats['nb_sessions'] * 100:.2f}%",
    font=("Arial", 16)
)
winrate.grid(row=4, column=0, columnspan=2, padx=30, pady=15)

launch_tracker_button = tk.Button(
    window,
    text="Lancer le tracker",
    font=("Arial", 16),
    command=launch_tracker
)


launch_tracker_button.pack(pady=20)





window.mainloop()