import customtkinter as ctk
import time

# Stopwatch state
tracker_on = False
start_time = None
start_bankroll = None


def update_chrono():
    """Update elapsed stopwatch display while tracker is running."""
    global tracker_on, start_time
    if not tracker_on or start_time is None:
        return
    elapsed = time.time() - start_time
    hrs = int(elapsed // 3600)
    mins = int((elapsed % 3600) // 60)
    secs = elapsed % 60
    chrono_label.configure(text=f"Session active  : {hrs:02d}:{mins:02d}:{secs:05.2f}")
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
    global tracker_on, start_time, start_bankroll
    try:
        end_bankroll = float(eb_entry.get())
    except Exception:
        end_bankroll = None

    if start_time is None:
        final_elapsed = 0.0
    else:
        final_elapsed = time.time() - start_time

    tracker_on = False
    hrs = int(final_elapsed // 3600)
    mins = int((final_elapsed % 3600) // 60)
    secs = final_elapsed % 60
    text = f"{hrs:02d}:{mins:02d}:{secs:05.2f}"
    if start_bankroll is not None and end_bankroll is not None:
        profit = end_bankroll - start_bankroll
        text += f"  |  Profit: {profit:+.2f}"
    chrono_label.configure(text=text)
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
frame.pack(fill="both", expand=True, padx=20, pady=20)

column1 = ctk.CTkFrame(
    frame,
    fg_color="#3a3a3a",
    border_width=1,
    border_color="#7a7a7a",
    corner_radius=18,
    height=250,
)
column1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

column2 = ctk.CTkFrame(
    frame,
    fg_color="#3a3a3a",
    border_width=1,
    border_color="#7a7a7a",
    corner_radius=18,
    height=250,
)
column2.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

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
    fg_color="#c92828",
    border_width=1,
    border_color="#6f6f6f",
    corner_radius=20,
    width=300,
    height=100,
    text="Stop Tracker",
    text_color="#000000",
    font=("Helvetica", 15, "bold"),
    hover_color="#741515",
    command=stop_window,
)
stop_session_button.grid(row=1, column=1, padx=10, pady=10)

chrono_label = ctk.CTkLabel(
    app,
    text="No session currently running ! ",
    font=("Helvetica", 15)

)

chrono_label.pack(padx = 10, pady=15)

app.mainloop()