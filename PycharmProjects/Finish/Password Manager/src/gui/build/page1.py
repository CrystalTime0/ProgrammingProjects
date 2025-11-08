# Thisc1next=Noneenerated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

import tkinter as tkinter
from pathlib import Path
from tkinter import *


class Page1(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)


# from tkinter import *
# Explicit imports to satisfy Flake8


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Raphaël\PycharmProjects\Password Manager\gui\build\assets\frame1")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def get_generateinfo():
    c1_generate_var = c1.get()
    c2_generate_var = c2.get()
    print(f"{c1_generate_var}\n{c2_generate_var}")


window = Tk()

window.geometry("430x480")
window.configure(bg="#BBC4C4")

canvas = Canvas(
    window,
    bg="#BBC4C4",
    height=480,
    width=430,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0)
canvas.create_rectangle(
    65.0,
    41.0,
    365.0,
    111.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    76.0,
    57.0,
    anchor="nw",
    text="Password Manager",
    fill="#000000",
    font=("InriaSerif Regular", 32 * -1)
)

global c1
global c2
c1 = IntVar()
c2 = IntVar()

c1digits = Checkbutton(window, text="Digits ?", height=2, width=10, variable=c1)
c1digits.place(
    x=140.0,
    y=170.0,
    width=150.0,
    height=50.0
)
c2punctuation = Checkbutton(window, text="Punctuation ?", height=2, width=10, variable=c2)
c2punctuation.place(
    x=140.0,
    y=250.0,
    width=150.0,
    height=50.0
)

"""
def two_fonc_bt_generate():
    print(get_generateinfo())
    print(parent.show_frame(Page2))
"""

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: parent.show_frame(Page2),
    relief="flat"
)
button_1.place(
    x=115.0,
    y=359.0,
    width=200.0,
    height=50.0
)
window.resizable(False, False)
window.mainloop()
from gui.build.page2 import Page2