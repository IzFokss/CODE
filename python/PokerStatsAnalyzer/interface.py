import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
import subprocess
import sys
import os
from datetime import datetime, timedelta

from stats import get_stats
import clean_sessions

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_FILE = "sessions.csv"
CLEANED_FILE = "sessions.cleaned.csv"
MIN_SESSION_DURATION = 30

tracker_process = None
manual_session_active = False
manual_session_start = None
manual_session_bankroll_start = None


def launch_tracker():
    global tracker_process, manual_session_active, manual_session_start, manual_session_bankroll_start

    if manual_mode_var.get():
        if manual_session_active:
            messagebox.showinfo("Tracker", "Une session manuelle est déjà en cours.")
            return

        start_bankroll = simpledialog.askstring(
            "Bankroll de début",
            "Entrez votre bankroll de début :",
            parent=window
        )

        if start_bankroll is None:
            return

        try:
            manual_session_bankroll_start = int(start_bankroll.replace(" ", ""))
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "La bankroll de début doit être un nombre entier."
            )
            return

        manual_session_start = datetime.now()
        manual_session_active = True
        manual_session_status_label.config(
            text=f"Session manuelle lancée à {manual_session_start.strftime('%Y-%m-%d %H:%M:%S')}"
        )
        manual_mode_toggle.config(state="disabled")
        messagebox.showinfo(
            "Tracker manuelle",
            "Session manuelle démarrée. Cliquez sur Stop tracker pour saisir la bankroll de fin."
        )
        return

    if tracker_process is not None and tracker_process.poll() is None:
        messagebox.showinfo("Tracker", "Le tracker est déjà lancé.")
        return

    tracker_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "tracker.py"
    )

    tracker_process = subprocess.Popen(
        [sys.executable, tracker_path]
    )
    messagebox.showinfo("Tracker", "Le tracker a été lancé.")


def stop_tracker():
    global tracker_process, manual_session_active, manual_session_start, manual_session_bankroll_start

    if manual_mode_var.get() and manual_session_active:
        end_bankroll = simpledialog.askstring(
            "Bankroll de fin",
            "Entrez votre bankroll de fin :",
            parent=window
        )

        if end_bankroll is None:
            return

        try:
            bankroll_end = int(end_bankroll.replace(" ", ""))
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "La bankroll de fin doit être un nombre entier."
            )
            return

        duration = int((datetime.now() - manual_session_start).total_seconds())
        profit = bankroll_end - manual_session_bankroll_start

        csv_path = os.path.join(BASE_DIR, SESSIONS_FILE)
        if not os.path.exists(csv_path):
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["session", "start", "end", "duration_seconds", "bankroll_start", "bankroll_end", "profit"])

        with open(csv_path, "r", encoding="utf-8") as f:
            session_number = len(f.readlines())

        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                session_number,
                manual_session_start.strftime("%Y-%m-%d %H:%M:%S"),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                duration,
                manual_session_bankroll_start,
                bankroll_end,
                profit,
            ])

        manual_session_active = False
        manual_session_start = None
        manual_session_bankroll_start = None
        manual_session_status_label.config(text="Aucune session manuelle en cours")
        manual_mode_toggle.config(state="normal")
        refresh_stats()

        messagebox.showinfo(
            "Tracker manuelle",
            f"Session manuelle terminée. Durée : {duration}s, Profit : {profit:,}"
        )
        return

    if tracker_process is None:
        messagebox.showinfo("Tracker", "Aucun tracker en cours d'exécution.")
        return

    if tracker_process.poll() is None:
        tracker_process.terminate()
        try:
            tracker_process.wait(timeout=5)
        except Exception:
            tracker_process.kill()
            tracker_process.wait()
        messagebox.showinfo("Tracker", "Le tracker a été arrêté.")

    tracker_process = None


def format_time(seconds):
    minutes, sec = divmod(seconds, 60)
    if minutes == 0:
        return f"{sec} seconds"
    hours, minutes = divmod(minutes, 60)
    if hours == 0:
        return f"{minutes} minutes {sec} seconds"
    return f"{hours} hours {minutes} minutes {sec} seconds"


def get_data_file():
    cleaned_path = os.path.join(BASE_DIR, CLEANED_FILE)
    default_path = os.path.join(BASE_DIR, SESSIONS_FILE)
    return cleaned_path if os.path.exists(cleaned_path) else default_path


def refresh_stats():
    stats_path = get_data_file()
    stats = get_stats(stats_path)

    data_source_label.config(
        text=f"Source: {os.path.basename(stats_path)}"
    )
    profit.config(text=f"Total profit: {stats['total_profit']:,}")
    sessions.config(text=f"Sessions: {stats['nb_sessions']}")
    time_played.config(
        text=f"Time played: {format_time(stats['total_time_played'])}"
    )
    avg_profit.config(
        text=f"Average profit per session: {stats['avg_profit_per_session']:,.2f}"
    )
    best_profit.config(
        text=f"Best session: {stats['best_session_profit']:,}")
    worst_profit.config(
        text=f"Worst session: {stats['worst_session_profit']:,}")
    win_sessions.config(
        text=f"Winning sessions: {len([p for p in stats['profits'] if p > 0])}"
    )
    loss_sessions.config(
        text=f"Losing sessions: {len([p for p in stats['profits'] if p < 0])}"
    )
    winrate.config(
        text=f"Win rate: {len([p for p in stats['profits'] if p > 0]) / stats['nb_sessions'] * 100:.2f}%"
    )


def parse_manual_datetime(value, default):
    if value is None:
        return default

    value = value.strip()
    if not value:
        return default

    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def save_manual_session():
    start_value = manual_start_entry.get()
    end_value = manual_end_entry.get()
    start_bankroll_value = manual_start_bankroll_entry.get()
    end_bankroll_value = manual_end_bankroll_entry.get()

    try:
        bankroll_start = int(start_bankroll_value.replace(" ", ""))
        bankroll_end = int(end_bankroll_value.replace(" ", ""))
    except ValueError:
        messagebox.showerror(
            "Erreur",
            "Veuillez entrer des bankrolls valides (entiers)."
        )
        return

    now = datetime.now()
    start_time = parse_manual_datetime(start_value, now - timedelta(hours=1))
    end_time = parse_manual_datetime(end_value, now)

    if start_time is None or end_time is None:
        messagebox.showerror(
            "Erreur",
            "Veuillez entrer une date valide au format YYYY-MM-DD HH:MM:SS."
        )
        return

    duration = int((end_time - start_time).total_seconds())
    if duration <= 0:
        messagebox.showerror(
            "Erreur",
            "La date de fin doit être après la date de début."
        )
        return

    if not os.path.exists(os.path.join(BASE_DIR, SESSIONS_FILE)):
        with open(os.path.join(BASE_DIR, SESSIONS_FILE), "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["session", "start", "end", "duration_seconds", "bankroll_start", "bankroll_end", "profit"])

    with open(os.path.join(BASE_DIR, SESSIONS_FILE), "r", encoding="utf-8") as f:
        lines = f.readlines()
        session_number = len(lines)

    with open(os.path.join(BASE_DIR, SESSIONS_FILE), "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            session_number,
            start_time.strftime("%Y-%m-%d %H:%M:%S"),
            end_time.strftime("%Y-%m-%d %H:%M:%S"),
            duration,
            bankroll_start,
            bankroll_end,
            bankroll_end - bankroll_start,
        ])

    messagebox.showinfo(
        "Session manuelle",
        "La session manuelle a été ajoutée avec succès."
    )
    refresh_stats()


def fix_sessions():
    try:
        input_path = os.path.join(BASE_DIR, SESSIONS_FILE)
        output_path = os.path.join(BASE_DIR, CLEANED_FILE)

        rows = clean_sessions.load_sessions(input_path)
        kept, removed, repaired = clean_sessions.clean_sessions(
            rows,
            min_duration=MIN_SESSION_DURATION,
            remove_zero_profit=False,
        )
        clean_sessions.write_sessions(output_path, kept)

        messagebox.showinfo(
            "Correction des sessions",
            f"Correction terminée.\nConservées : {len(kept)}\nSupprimées : {len(removed)}\nRéparées : {len(repaired)}"
        )
        refresh_stats()
    except Exception as e:
        messagebox.showerror(
            "Erreur",
            f"Impossible de corriger les sessions : {e}"
        )


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

manual_mode_var = tk.BooleanVar(value=False)

toggle_frame = tk.Frame(window)
toggle_frame.pack(pady=(0, 10))

toggle_label = tk.Label(
    toggle_frame,
    text="Mode saisie manuelle :",
    font=("Arial", 12)
)
toggle_label.pack(side="left", padx=(0, 10))

manual_mode_toggle = tk.Checkbutton(
    toggle_frame,
    variable=manual_mode_var,
    text="Activé",
    font=("Arial", 12),
    command=lambda: manual_frame.pack(pady=(0, 15)) if manual_mode_var.get() else manual_frame.pack_forget()
)
manual_mode_toggle.pack(side="left")


data_source_label = tk.Label(
    window,
    text=f"Source: {os.path.basename(get_data_file())}",
    font=("Arial", 12)
)
data_source_label.pack(pady=(10, 10))

manual_frame = tk.Frame(window)
manual_frame.pack_forget()

manual_start_label = tk.Label(
    manual_frame,
    text="Début de session (YYYY-MM-DD HH:MM:SS)",
    font=("Arial", 12)
)
manual_start_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
manual_start_entry = tk.Entry(manual_frame, width=25, font=("Arial", 12))
manual_start_entry.grid(row=0, column=1, padx=10, pady=2)

manual_end_label = tk.Label(
    manual_frame,
    text="Fin de session (YYYY-MM-DD HH:MM:SS)",
    font=("Arial", 12)
)
manual_end_label.grid(row=1, column=0, sticky="w", padx=10, pady=2)
manual_end_entry = tk.Entry(manual_frame, width=25, font=("Arial", 12))
manual_end_entry.grid(row=1, column=1, padx=10, pady=2)

manual_start_bankroll_label = tk.Label(
    manual_frame,
    text="Bankroll début",
    font=("Arial", 12)
)
manual_start_bankroll_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)
manual_start_bankroll_entry = tk.Entry(manual_frame, width=25, font=("Arial", 12))
manual_start_bankroll_entry.grid(row=2, column=1, padx=10, pady=2)

manual_end_bankroll_label = tk.Label(
    manual_frame,
    text="Bankroll fin",
    font=("Arial", 12)
)
manual_end_bankroll_label.grid(row=3, column=0, sticky="w", padx=10, pady=2)
manual_end_bankroll_entry = tk.Entry(manual_frame, width=25, font=("Arial", 12))
manual_end_bankroll_entry.grid(row=3, column=1, padx=10, pady=2)

manual_save_button = tk.Button(
    manual_frame,
    text="Enregistrer session manuelle",
    font=("Arial", 12),
    command=save_manual_session
)
manual_save_button.grid(row=4, column=0, columnspan=2, pady=(10, 0))

manual_session_status_label = tk.Label(
    window,
    text="Aucune session manuelle en cours",
    font=("Arial", 12),
    fg="blue"
)
manual_session_status_label.pack(pady=(0, 10))

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


stats = get_stats(get_data_file())
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

fix_sessions_button = tk.Button(
    button_frame,
    text="Corriger sessions",
    font=("Arial", 16),
    command=fix_sessions
)

launch_tracker_button.pack(side="left", padx=(0, 10))
stop_tracker_button.pack(side="left", padx=(0, 10))
fix_sessions_button.pack(side="left")





window.mainloop()