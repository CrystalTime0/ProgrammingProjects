import tkinter as tk
from tkinter import *
window = tk.Tk()
window.title("Cookie Clicker")
window.geometry("570x800+100+200")
window.resizable(False, False)
window.configure(bg="#181818")

ccl = "2**(l1/2)"

print(f"{ccl} egal : {eval(ccl)}")

label_text_str = (
    Label(window, width=25, height=1, text=ccl, bg="#181818", fg="#fff", font=("arial", 40)))
label_text_str.place(x=-100, y=100)

label_result = (
    Label(window, width=25, height=1, text=eval(ccl), bg="#181818", fg="#fff", font=("arial", 40)))
label_result.place(x=-100, y=200)

window.mainloop()