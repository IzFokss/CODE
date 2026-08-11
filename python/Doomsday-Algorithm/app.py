import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Doomsday Algorithm")
root.geometry("400x300")


def doomsday_for_date(date_str: str) -> str:
    """Return weekday name for YYYY-MM-DD using the Doomsday algorithm."""
    day_index = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    try:
        year, month, day = map(int, date_str.split('-'))
    except Exception:
        raise ValueError("Date must be in YYYY-MM-DD format")

    # Century anchors (for centuries 1500..2699)
    years_doomsday_index = {
        15: 3, 16: 2, 17: 0, 18: 5,
        19: 3, 20: 2, 21: 0, 22: 5,
        23: 3, 24: 2, 25: 0, 26: 5
    }

    century = year // 100
    if century not in years_doomsday_index:
        raise ValueError("Year out of supported range for century anchor")

    anchor = years_doomsday_index[century]
    y = year % 100
    a = y // 12
    b = y % 12
    c = b // 4
    doomsday = (anchor + a + b + c) % 7

    # Leap year handling
    is_leap = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

    month_doomsday = {
        1: 4 if is_leap else 3,
        2: 29 if is_leap else 28,
        3: 7,
        4: 4,
        5: 9,
        6: 6,
        7: 11,
        8: 8,
        9: 5,
        10: 10,
        11: 7,
        12: 12,
    }

    if month not in month_doomsday:
        raise ValueError("Invalid month")

    diff = day - month_doomsday[month]
    weekday_index = (doomsday + diff) % 7
    return day_index[weekday_index]


def calculate_doomsday():
    date_str = input_entry.get().strip()
    try:
        weekday = doomsday_for_date(date_str)
        messagebox.showinfo("Result", f"{date_str} was a {weekday}.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Label for the date
label = tk.Label(root, text="Enter a date (YYYY-MM-DD):")
label.pack(pady=10)
# input
input_entry = tk.Entry(root)
input_entry.pack(pady=10)
# calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_doomsday)
calculate_button.pack(pady=10)


if __name__ == '__main__':
    root.mainloop()
