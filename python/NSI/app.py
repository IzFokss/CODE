import customtkinter as ctk
from tkinter import messagebox




app = ctk.CTk()
app.geometry("400x300")
def show_message():
    messagebox.showinfo("Information", "This is a message box!")


app.mainloop()