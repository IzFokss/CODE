import customtkinter as ctk
import time
import csv 
import os 


# Stopwatch state
tracker_on = False
start_time = None
stopped_elapsed = None
start_bankroll = None





def get_stats_csv_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "poker_stats.csv")

def reset_stats():
    fieldnames = ["sbankroll","ebankroll","profit","duration"]
    with open('poker_stats.csv',"w",newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()


def calculate_stats():
    csv_path = get_stats_csv_path()
    if not os.path.exists(csv_path):
        return {
            "total_profit": 0,
            "nb_sessions": 0,
            "avg_profit": 0,
            "total_duration": 0,
            "profitable_sessions": 0,
            "losing_sessions": 0,
            "winrate": 0,
            "best_session": 0,
            "profit_per_hour": 0,
            "avg_session_duration": 0,
        }

    with open(csv_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)

        total_profit = 0
        nb_sessions = 0
        avg_profit_per_session = 0
        total_duration = 0
        profitable_sessions = 0
        losing_sessions = 0
        winrate = 0
        best_session = 0
        worst_session = 0
        avg_winning_session = 0
        avg_losing_session = 0
        avg_session_duration = 0
        profit_per_hour = 0

        for row in reader:
            profit = float(row['profit'])
            

            total_profit += profit
            nb_sessions += 1
            total_duration += float(row['duration'])
            avg_session_duration = total_duration / nb_sessions

            if profit > 0:
                profitable_sessions += 1
                avg_winning_session =  (avg_winning_session + profit)/profitable_sessions
            elif profit < 0:
                losing_sessions += 1
                avg_losing_session =  (avg_losing_session + profit)/losing_sessions

            if profit > best_session:
                best_session = profit
            elif profit < worst_session:
                worst_session = profit

        if nb_sessions > 0:
            avg_profit_per_session = total_profit / nb_sessions
            winrate = (profitable_sessions / nb_sessions) * 100
        if total_duration > 0:
            profit_per_hour = total_profit / (total_duration / 3600)
        

        return {
            "total_profit": total_profit,
            "nb_sessions": nb_sessions,
            "avg_profit": avg_profit_per_session,
            "total_duration": total_duration,
            "profitable_sessions": profitable_sessions,
            "losing_sessions": losing_sessions,
            "winrate": winrate,
            "best_session": best_session,
            "profit_per_hour": profit_per_hour,
            "avg_session_duration" : avg_session_duration
    }


def format_duration(seconds):
    seconds = int(seconds)
    if seconds >= 3600:
        hrs = seconds // 3600
        mins = (seconds % 3600) // 60
        return f"{hrs}h {mins}m"
    if seconds >= 60:
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins}m {secs}s"
    return f"{seconds}s"


def update_stats():
    stats = calculate_stats()

    tp_label.configure(text=f"Total Profit : ${stats['total_profit']:.2f}")
    nb_sessions_label.configure(text=f"Number of sessions : {stats['nb_sessions']}")
    avg_profit_label.configure(text=f"Avg profit / session : ${stats['avg_profit']:.2f}")
    total_duration_label.configure(text=f"Total duration : {format_duration(stats['total_duration'])}")
    profitable_sessions_label.configure(text=f"Profitable sessions : {stats['profitable_sessions']}")
    losing_sessions_label.configure(text=f"Losing sessions : {stats['losing_sessions']}")
    winrate_label.configure(text=f"Winrate : {stats['winrate']:.1f}%")
    best_session_label.configure(text=f"Best session : ${stats['best_session']:.2f}")
    profit_per_hour_label.configure(text=f"Profit / hour : ${stats['profit_per_hour']:.2f}")
    avg_session_duration_label.configure(text=f"Average session duration : {format_duration(stats['avg_session_duration'])}")
    update_last_session_stats()


def update_last_session_stats():
    csv_path = get_stats_csv_path()
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        lss_sb.configure(text="Start bankroll : $0.00")
        lss_eb.configure(text="End bankroll : $0.00")
        lss_profit.configure(text="Profit : $0.00")
        lss_duration.configure(text="Duration : 0s")
        return

    with open(csv_path, 'r', newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))

    if not rows:
        lss_sb.configure(text="Start bankroll : $0.00")
        lss_eb.configure(text="End bankroll : $0.00")
        lss_profit.configure(text="Profit : $0.00")
        lss_duration.configure(text="Duration : 0s")
        return

    last_row = rows[-1]
    start_bankroll_value = float(last_row['sbankroll'])
    end_bankroll_value = float(last_row['ebankroll'])
    profit_value = float(last_row['profit'])
    duration_value = float(last_row['duration'])

    lss_sb.configure(text=f"Start bankroll : ${start_bankroll_value:.2f}")
    lss_eb.configure(text=f"End bankroll : ${end_bankroll_value:.2f}")
    lss_profit.configure(text=f"Profit : ${profit_value:+.2f}")
    lss_duration.configure(text=f"Duration : {format_duration(duration_value)}")


def save_in_csv(sbankroll,ebankroll,profit,duration):
    data = [{
        'sbankroll' : sbankroll,
        'ebankroll' : ebankroll,
        'profit' : profit,
        'duration' : duration
    }

    ]
    csv_path = get_stats_csv_path()
    with open(csv_path, "a", newline='') as csvfile:
        fieldnames = ["sbankroll","ebankroll","profit","duration"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if os.path.getsize(csv_path) == 0:
            writer.writeheader()
        writer.writerows(data)


def set_session_status(state, elapsed=None):
    if state == "running":
        if elapsed is None:
            elapsed = time.time() - start_time
        hrs = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        secs = elapsed % 60
        chrono_label.configure(text=f"Status: Running | {hrs:02d}:{mins:02d}:{secs:05.2f}")
    elif state == "stopped":
        if elapsed is None:
            elapsed = 0
        hrs = int(elapsed // 3600)
        mins = int((elapsed % 3600) // 60)
        secs = elapsed % 60
        chrono_label.configure(text=f"Status: Stopped | {hrs:02d}:{mins:02d}:{secs:05.2f}")
    else:
        chrono_label.configure(text="Status: Idle | No active session")


def update_chrono():
    """Update elapsed stopwatch display while tracker is running."""
    global tracker_on, start_time
    if not tracker_on or start_time is None:
        return
    elapsed = time.time() - start_time
    set_session_status("running", elapsed)
    app.after(50, update_chrono)


def start_tracker(sb_entry, bw):
    """Start a session: record bankroll and start time, begin updates."""
    global start_time, tracker_on, start_bankroll

    sb = sb_entry.get()
    try:
        start_bankroll = float(sb)
    except Exception:
        start_bankroll = None

    start_time = time.time()
    tracker_on = True

    bw.destroy()
    set_session_status("running", 0.0)
    update_chrono()


def start_window():
    bw = ctk.CTkToplevel(app)
    bw.geometry("300x200")
    bw.title("Enter Bankroll")
    bw.resizable(False, False)
    bw.attributes("-alpha", 0.96)

    header = ctk.CTkLabel(
        bw,
        text="Start bankroll",
        fg_color="#4d4d4d",
        border_width=1,
        border_color="#7a7a7a",
        width=300,
        height=50,
        font=("Helvetica", 14, "bold"),
        corner_radius=12,
        text_color="#f5f5f5",
    )
    header.pack(pady=15, padx=20, fill="x")

    sb_entry = ctk.CTkEntry(
        bw,
        placeholder_text='Start Bankroll',
        justify='center',
        width=300,
    )
    sb_entry.pack(pady=15, padx=20)
    vb_button = ctk.CTkButton(
        bw,
        width=300,
        height=75,
        corner_radius=20,
        fg_color="#000200",
        hover_color="#001700",
        text_color='#ffffff',
        text="Start session",
        command=lambda: start_tracker(sb_entry, bw),
    )
    vb_button.pack(pady=15, padx=20)


def stop_window():
    """Open dialog to enter end bankroll and stop the session."""
    global tracker_on, start_time, stopped_elapsed

    if start_time is not None:
        stopped_elapsed = time.time() - start_time
        hrs = int(stopped_elapsed // 3600)
        mins = int((stopped_elapsed % 3600) // 60)
        secs = stopped_elapsed % 60
        chrono_label.configure(text=f"Status: Stopped | {hrs:02d}:{mins:02d}:{secs:05.2f}")

    tracker_on = False

    bw = ctk.CTkToplevel(app)
    bw.geometry("300x200")
    bw.title("End bankroll")
    bw.resizable(False, False)
    bw.attributes("-alpha", 0.96)
    header = ctk.CTkLabel(
        bw,
        text="End bankroll",
        fg_color="#4d4d4d",
        border_width=1,
        border_color="#7a7a7a",
        width=300,
        height=50,
        font=("Helvetica", 14, "bold"),
        corner_radius=12,
        text_color="#f5f5f5",
    )
    header.pack(pady=15, padx=20, fill='x')
    eb_entry = ctk.CTkEntry(
        bw,
        placeholder_text='End Bankroll',
        justify='center',
        width=300,
    )
    eb_entry.pack(pady=15, padx=20)
    vb_button = ctk.CTkButton(
        bw,
        width=300,
        height=75,
        corner_radius=20,
        fg_color="#000200",
        hover_color="#001700",
        text_color='#ffffff',
        text="Stop session",
        command=lambda: stop_tracker(eb_entry, bw),
    )
    vb_button.pack(pady=15, padx=20)


def stop_tracker(eb_entry, bw):
    """Stop the tracker, compute elapsed and profit, update label, close dialog."""
    global tracker_on, start_time, stopped_elapsed, start_bankroll
    try:
        end_bankroll = float(eb_entry.get())
    except Exception:
        end_bankroll = None

    if stopped_elapsed is not None:
        final_elapsed = stopped_elapsed
    elif start_time is None:
        final_elapsed = 0.0
    else:
        final_elapsed = time.time() - start_time

    tracker_on = False
    hrs = int(final_elapsed // 3600)
    mins = int((final_elapsed % 3600) // 60)
    secs = final_elapsed % 60
    text = f"{hrs:02d}:{mins:02d}:{secs:05.2f}"
    profit = 0.0
    if start_bankroll is not None and end_bankroll is not None:
        profit = end_bankroll - start_bankroll
        text += f"  |  Profit: {profit:+.2f}"
    chrono_label.configure(text=f"Status: Stopped | {text}")
    if start_bankroll is not None and end_bankroll is not None:
        save_in_csv(start_bankroll, end_bankroll, profit, final_elapsed)
        update_stats()
        start_time = None
        stopped_elapsed = None
        start_bankroll = None
    bw.destroy()



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("900x600")
app.title("PokerStatsAnalyzer")
app.resizable(False, False)
app.attributes("-alpha", 0.97)


title = ctk.CTkLabel(
    app,
    text="PokerStatsAnalyzer",
    fg_color="#4b4b4b",
    border_width=1,
    border_color="#7a7a7a",
    width=700,
    height=90,
    font=("Helvetica", 30, "bold"),
    corner_radius=16,
    text_color="#f7f7f7",
)
title.pack(pady=15)

frame = ctk.CTkFrame(
    app,
    width=700,
    height=500,
    border_color="#7a7a7a",
    border_width=1,
    corner_radius=22,
    fg_color="#2f2f2f",
)
frame.grid_columnconfigure(0, weight=2)
frame.grid_columnconfigure(1, weight=1)
frame.pack(fill="x", padx=20, pady=(15, 10))

column1 = ctk.CTkFrame(
    frame,
    fg_color="#3a3a3a",
    border_width=1,
    border_color="#7a7a7a",
    corner_radius=18,
    height=250,
)
column1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

stats_frame = ctk.CTkFrame(
    column1,
    fg_color="#3a3a3a",
    border_width=0,
)
stats_frame.pack(fill="both", expand=True, padx=10, pady=10)

stats_frame.grid_columnconfigure(0, weight=1)
stats_frame.grid_columnconfigure(1, weight=1)

tp_label = ctk.CTkLabel(
    stats_frame,
    text="Total Profit : 0"
)
tp_label.grid(row=0, column=0, sticky="w", padx=5, pady=4)

nb_sessions_label = ctk.CTkLabel(
    stats_frame,
    text="0 sessions"
)
nb_sessions_label.grid(row=0, column=1, sticky="w", padx=5, pady=4)

avg_profit_label = ctk.CTkLabel(
    stats_frame,
    text="Avg profit / session : $0.00"
)
avg_profit_label.grid(row=1, column=0, sticky="w", padx=5, pady=4)

total_duration_label = ctk.CTkLabel(
    stats_frame,
    text="Total duration : 0s"
)
total_duration_label.grid(row=1, column=1, sticky="w", padx=5, pady=4)

profitable_sessions_label = ctk.CTkLabel(
    stats_frame,
    text="Profitable sessions : 0"
)
profitable_sessions_label.grid(row=2, column=0, sticky="w", padx=5, pady=4)

losing_sessions_label = ctk.CTkLabel(
    stats_frame,
    text="Losing sessions : 0"
)
losing_sessions_label.grid(row=2, column=1, sticky="w", padx=5, pady=4)

winrate_label = ctk.CTkLabel(
    stats_frame,
    text="Winrate : 0.0%"
)
winrate_label.grid(row=3, column=0, sticky="w", padx=5, pady=4)

best_session_label = ctk.CTkLabel(
    stats_frame,
    text="Best session : $0.00"
)
best_session_label.grid(row=3, column=1, sticky="w", padx=5, pady=4)

profit_per_hour_label = ctk.CTkLabel(
    stats_frame,
    text="Profit / hour : $0.00"
)
profit_per_hour_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=5, pady=4)

avg_session_duration_label = ctk.CTkLabel(
    stats_frame,
    text="Average session duration : 0s"
)
avg_session_duration_label.grid(row=5,column=0,columnspan=2,sticky="w",padx=5,pady=4)

column2 = ctk.CTkFrame(
    frame,
    fg_color="#3a3a3a",
    border_width=1,
    border_color="#7a7a7a",
    corner_radius=18,
    height=250,
)
column2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

last_session_stats_frame = ctk.CTkFrame(
    column2,
    fg_color="#3a3a3a",
    border_width=0
)
last_session_stats_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
last_session_stats_frame.grid_columnconfigure(0, weight=1)
last_session_stats_frame.grid_columnconfigure(1, weight=1)

lss_sb = ctk.CTkLabel(
    last_session_stats_frame,
    text="Start bankroll : $0.00",
)
lss_sb.grid(row=0, column=0, sticky="w", pady=4, padx=4)

lss_eb = ctk.CTkLabel(
    last_session_stats_frame,
    text="End bankroll : $0.00"
)
lss_eb.grid(row=0, column=1, sticky="w", padx=4, pady=4)

lss_profit = ctk.CTkLabel(
    last_session_stats_frame,
    text="Profit : $0.00"
)
lss_profit.grid(row=1, column=0, columnspan=2, sticky="w", padx=4, pady=4)

lss_duration = ctk.CTkLabel(
    last_session_stats_frame,
    text="Duration : 0s"
)
lss_duration.grid(row=2, column=0, columnspan=2, sticky="w", pady=4, padx=4)


start_session_button = ctk.CTkButton(
    frame,
    fg_color="#32f800",
    border_width=1,
    border_color="#6f6f6f",
    corner_radius=20,
    width=300,
    height=100,
    text="Start Tracker",
    text_color="#000000",
    font=("Helvetica", 15, "bold"),
    hover_color="#287017",
    command=start_window,
)
start_session_button.grid(row=1, column=0, padx=10, pady=10)

stop_session_button = ctk.CTkButton(
    frame,
    fg_color="#182cdf",
    border_width=1,
    border_color="#6f6f6f",
    corner_radius=20,
    width=300,
    height=100,
    text="Stop Tracker",
    text_color="#000000",
    font=("Helvetica", 15, "bold"),
    hover_color="#09136d",
    command=stop_window,
)
stop_session_button.grid(row=1, column=1, padx=10, pady=10)

reset_all_stats_button = ctk.CTkButton(
    frame,
    fg_color="#c92828",
    border_width=1,
    border_color="#6f6f6f",
    corner_radius=20,
    width=50,
    height=50,
    text="Reset Stats",
    text_color="#000000",
    font=("Helvetica", 15, "bold"),
    hover_color="#5a0a0a",
    command=reset_stats,
)
reset_all_stats_button.grid(row=1, column=0,columnspan=2 ,padx=10, pady=10)

chrono_label = ctk.CTkLabel(
    app,
    text="Status: Idle | No active session",
    font=("Helvetica", 15),
    fg_color="#3a3a3a",
    corner_radius=8,
    padx=10,
    pady=6,
)

chrono_label.pack(padx=10, pady=(0, 10))



update_stats()





app.mainloop()