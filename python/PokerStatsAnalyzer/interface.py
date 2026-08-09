import tkinter as tk
import subprocess
import sys
import os
from datetime import datetime

from stats import get_stats

tracker_process = None


def launch_tracker():
    global tracker_process

    if tracker_process is not None and tracker_process.poll() is None:
        return

    tracker_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tracker.py"
    )

    tracker_process = subprocess.Popen(
        [sys.executable, tracker_path]
    )


def stop_tracker():
    global tracker_process

    if tracker_process is None:
        return

    if tracker_process.poll() is None:
        tracker_process.terminate()
        try:
            tracker_process.wait(timeout=5)
        except Exception:
            tracker_process.kill()
            tracker_process.wait()

    tracker_process = None


def format_time(seconds):
    minutes, sec = divmod(seconds, 60)
    if minutes == 0:
        return f"{sec} seconds"
    hours, minutes = divmod(minutes, 60)
    if hours == 0:
        return f"{minutes} minutes {sec} seconds"
    return f"{hours} hours {minutes} minutes {sec} seconds"


def get_last_session_stats():
    log_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tracker.log"
    )

    if not os.path.exists(log_path):
        return None

    last_session = None
    current_start = None

    with open(log_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if "SESSION START | Bankroll=" in line:
                try:
                    start_time = datetime.strptime(
                        line[1:20],
                        "%Y-%m-%d %H:%M:%S"
                    )
                    bankroll_start = int(
                        line.split("Bankroll=")[1]
                    )
                    current_start = {
                        "time": start_time,
                        "bankroll_start": bankroll_start
                    }
                except Exception:
                    current_start = None

            elif "SESSION TERMINÉE |" in line:
                try:
                    end_time = datetime.strptime(
                        line[1:20],
                        "%Y-%m-%d %H:%M:%S"
                    )
                    parts = [part.strip() for part in line.split("|")[1:]]
                    start_bankroll = int(parts[0].split("=")[1])
                    end_bankroll = int(parts[1].split("=")[1])
                    profit = int(parts[2].split("=")[1])

                    duration_seconds = None
                    if current_start is not None:
                        duration_seconds = int(
                            (end_time - current_start["time"]).total_seconds()
                        )

                    last_session = {
                        "start_time": current_start["time"] if current_start else None,
                        "start_bankroll": start_bankroll,
                        "end_time": end_time,
                        "end_bankroll": end_bankroll,
                        "profit": profit,
                        "duration_seconds": duration_seconds
                    }
                except Exception:
                    pass
                finally:
                    current_start = None

    return last_session


window = tk.Tk()

window.title("Zynga Poker Tracker")
window.geometry("1600x900")

title = tk.Label(
    window,
    text="ZYNGA POKER TRACKER",
    font=("Arial", 24)
)

title.pack(pady=30)

stats_frame = tk.Frame(window)
stats_frame.pack(pady=20)

general_stats_frame = tk.LabelFrame(
    stats_frame,
    text="General stats",
    font=("Arial", 16, "bold"),
    padx=10,
    pady=10,
    bd=2,
    relief="solid"
)
general_stats_frame.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")


stats = get_stats()
last_session = get_last_session_stats()


profit = tk.Label(
    general_stats_frame,
    text=f"Total profit: {stats['total_profit']:,}",
    font=("Arial", 16)
)

profit.grid(row=0, column=0, padx=30, pady=15)


sessions = tk.Label(
    general_stats_frame,
    text=f"Sessions: {stats['nb_sessions']}",
    font=("Arial", 16)
)

sessions.grid(row=0, column=1, padx=30, pady=15)


time_played = tk.Label(
    general_stats_frame,
    text=f"Time played: {format_time(stats['total_time_played'])}",
    font=("Arial", 16)
)

time_played.grid(row=1, column=0, padx=30, pady=15)



avg_profit = tk.Label(
    general_stats_frame,
    text=f"Average profit per session: {stats['avg_profit_per_session']:,.2f}",
    font=("Arial", 16)
)
avg_profit.grid(row=1, column=1, padx=30, pady=15)

best_profit = tk.Label(
    general_stats_frame,
    text=f"Best session: {stats['best_session_profit']:,}",
    font=("Arial", 16)
)

best_profit.grid(row=2, column=0, padx=30, pady=15)

worst_profit = tk.Label(
    general_stats_frame,
    text=f"Worst session: {stats['worst_session_profit']:,}",
    font=("Arial", 16)
)
worst_profit.grid(row=2, column=1, padx=30, pady=15)

win_sessions = tk.Label(
    general_stats_frame,
    text=f"Winning sessions: {len([p for p in stats['profits'] if p > 0])}",
    font=("Arial", 16)
)
win_sessions.grid(row=3, column=0, padx=30, pady=15)

loss_sessions = tk.Label(
    general_stats_frame,
    text=f"Losing sessions: {len([p for p in stats['profits'] if p < 0])}",
    font=("Arial", 16)
)
loss_sessions.grid(row=3, column=1, padx=30, pady=15)

winrate = tk.Label(
    general_stats_frame,
    text=f"Win rate: {len([p for p in stats['profits'] if p > 0]) / stats['nb_sessions'] * 100:.2f}%",
    font=("Arial", 16)
)
winrate.grid(row=4, column=0, columnspan=2, padx=30, pady=15)

last_session_frame = tk.LabelFrame(
    stats_frame,
    text="Last session",
    font=("Arial", 16, "bold"),
    padx=10,
    pady=10
)
last_session_frame.grid(row=5, column=0, columnspan=2, padx=30, pady=15, sticky="w")

if last_session is None:
    last_session_message = tk.Label(
        last_session_frame,
        text="No completed session data",
        font=("Arial", 16),
        justify="left",
        anchor="w"
    )
    last_session_message.pack(anchor="w")
else:
    duration_text = (
        format_time(last_session["duration_seconds"])
        if last_session["duration_seconds"] is not None
        else "Unknown duration"
    )

    last_session_duration = tk.Label(
        last_session_frame,
        text=f"Duration: {duration_text}",
        font=("Arial", 16),
        justify="left",
        anchor="w"
    )
    last_session_profit = tk.Label(
        last_session_frame,
        text=f"Profit: {last_session['profit']:,}",
        font=("Arial", 16),
        justify="left",
        anchor="w"
    )
    last_session_start = tk.Label(
        last_session_frame,
        text=f"Start bankroll: {last_session['start_bankroll']:,}",
        font=("Arial", 16),
        justify="left",
        anchor="w"
    )
    last_session_end = tk.Label(
        last_session_frame,
        text=f"End bankroll: {last_session['end_bankroll']:,}",
        font=("Arial", 16),
        justify="left",
        anchor="w"
    )

    last_session_duration.pack(anchor="w")
    last_session_profit.pack(anchor="w")
    last_session_start.pack(anchor="w")
    last_session_end.pack(anchor="w")

button_frame = tk.Frame(window)
button_frame.pack(pady=10)

launch_tracker_button = tk.Button(
    button_frame,
    text="Launch tracker",
    font=("Arial", 16),
    command=launch_tracker
)

stop_tracker_button = tk.Button(
    button_frame,
    text="Stop tracker",
    font=("Arial", 16),
    command=stop_tracker
)

launch_tracker_button.pack(side="left", padx=(0, 10))
stop_tracker_button.pack(side="left")





window.mainloop()