import time
from tkinter import *
import tkinter as tk
from time import *

window = tk.Tk()

window.title("Cookie Clicker")
window.geometry("570x800+100+200")
window.resizable(False, False)
window.configure(bg="#181818")

nb_cookies = 0


def add_cookies(nb):
    global nb_cookies
    nb_cookies += nb
    label_nb_cookies.config(text=nb_cookies)


label_nb_cookies = (
    Label(window, width=25, height=1, text=nb_cookies, bg="#181818", fg="#fff", font=("arial", 40)))
label_nb_cookies.place(x=-100, y=100)

dqd = Button(window, text="C", width=10, height=2, font=("arial", 30, "bold"), bd=2, fg="#fff", bg="#181818",
             command=lambda: add_cookies(1)).place(x=150, y=300)
window.mainloop()
