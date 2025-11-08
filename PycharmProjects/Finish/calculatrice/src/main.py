from tkinter import *
import tkinter as tk

window = tk.Tk()

window.title("Calculator")
window.geometry("570x600+100+200")
window.resizable(False, False)
window.configure(bg="#181818")

light_mode = Frame(window, bg="#d6d6d6")
light_mode.place(x=0, y=0, width=1000, height=600)
dark_mode = Frame(window, bg="#101010")
dark_mode.place(x=0, y=0, width=1000, height=600)

dark_mode.tkraise()

label_resultD = Label(dark_mode, width=25, height=2, text="", bg="#202020", fg="#fff", font=("arial", 30))
label_resultD.place(x=0, y=0)
label_resultL = Label(light_mode, width=25, height=2, text="", bg="#e4e4e4", fg="#000", font=("arial", 30))
label_resultL.place(x=0, y=0)

equation = ""
bg_dark_button = "#2a2d36"
bg_light_button = "#e3e3e3"
mode = "dark"


def change_mode():
    global mode
    if mode == "dark":
        light_mode.tkraise()
        mode = "light"
        label_resultL.config(text=equation)
    elif mode == "light":
        dark_mode.tkraise()
        mode = "dark"
        label_resultD.config(text=equation)


def show(item):
    global equation
    if equation != "0":
        equation += item
    else:
        if item.isdigit():
            equation = item
        else:
            equation += item
    if mode == "dark":
        label_resultD.config(text=equation)
    elif mode == "light":
        label_resultL.config(text=equation)


def clear():
    global equation, mode
    equation = ""
    if mode == "dark":
        label_resultD.config(text=equation)
    elif mode == "light":
        label_resultL.config(text=equation)


def calculate():
    global equation, mode
    result = ""
    if equation != "":
        try:
            result = eval(equation)
            equation = str(result)
        except:
            result = "Error"
            equation = ""
    if mode == "dark":
        label_resultD.config(text=result)
    elif mode == "light":
        label_resultL.config(text=result)


Button(light_mode, text="C", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: clear()).place(x=10, y=100)
Button(light_mode, text="/", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("/")).place(x=150, y=100)
Button(light_mode, text="%", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("%")).place(x=290, y=100)
Button(light_mode, text="*", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("*")).place(x=430, y=100)

Button(light_mode, text="7", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("7")).place(x=10, y=200)
Button(light_mode, text="8", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("8")).place(x=150, y=200)
Button(light_mode, text="9", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("9")).place(x=290, y=200)
Button(light_mode, text="-", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("-")).place(x=430, y=200)

Button(light_mode, text="4", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("4")).place(x=10, y=300)
Button(light_mode, text="5", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("5")).place(x=150, y=300)
Button(light_mode, text="6", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("6")).place(x=290, y=300)
Button(light_mode, text="+", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("+")).place(x=430, y=300)

Button(light_mode, text="1", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("1")).place(x=10, y=400)
Button(light_mode, text="2", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("2")).place(x=150, y=400)
Button(light_mode, text="3", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("3")).place(x=290, y=400)

Button(light_mode, text="=", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg="#fe9037",
       command=lambda: calculate()).place(x=430, y=400)
Button(light_mode, text="< >", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg="#fe9037",
       command=lambda: change_mode()).place(x=430, y=500)

Button(light_mode, text="0", width=11, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show("0")).place(x=10, y=500)
Button(light_mode, text=".", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#000", bg=bg_light_button,
       command=lambda: show(".")).place(x=290, y=500)


Button(dark_mode, text="C", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: clear()).place(x=10, y=100)
Button(dark_mode, text="/", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("/")).place(x=150, y=100)
Button(dark_mode, text="%", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("%")).place(x=290, y=100)
Button(dark_mode, text="*", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("*")).place(x=430, y=100)

Button(dark_mode, text="7", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("7")).place(x=10, y=200)
Button(dark_mode, text="8", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("8")).place(x=150, y=200)
Button(dark_mode, text="9", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("9")).place(x=290, y=200)
Button(dark_mode, text="-", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("-")).place(x=430, y=200)

Button(dark_mode, text="4", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("4")).place(x=10, y=300)
Button(dark_mode, text="5", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("5")).place(x=150, y=300)
Button(dark_mode, text="6", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("6")).place(x=290, y=300)
Button(dark_mode, text="+", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("+")).place(x=430, y=300)

Button(dark_mode, text="1", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("1")).place(x=10, y=400)
Button(dark_mode, text="2", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("2")).place(x=150, y=400)
Button(dark_mode, text="3", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("3")).place(x=290, y=400)

Button(dark_mode, text="=", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg="#fe9037",
       command=lambda: calculate()).place(x=430, y=400)
Button(dark_mode, text="< >", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg="#fe9037",
       command=lambda: change_mode()).place(x=430, y=500)

Button(dark_mode, text="0", width=11, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show("0")).place(x=10, y=500)
Button(dark_mode, text=".", width=5, height=1, font=("arial", 30, "bold"), bd=2, fg="#fff", bg=bg_dark_button,
       command=lambda: show(".")).place(x=290, y=500)

window.mainloop()
