import numpy as np
import pandas as pd
import matplotlib.figure
import matplotlib.pyplot as plt
from tkinter import Tk, Frame, Label, Text, Button, END
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

pos = 0
b = 0
mistakes = 0
correct_presses = 0
typing_speed = 0
duration = 0
start_time = 0
end_time = 0
minutes = 0
seconds = 0


def handle_stats():
    global typing_speed, correct_presses, mistakes
    entries = correct_presses + mistakes
    typing_speed = (entries / 5) / 1
    duration_label = Label(
        window,
        text=get_duration(),
        font=("Arial ", 16)
    )
    typing_speed_label = Label(
        window,
        text="Typing speed: " + str(int(typing_speed)) + " WPM",
        font=("Arial ", 16)
    )
    duration_label.pack()
    typing_speed_label.pack()


def draw_pie_chart():
    global mistakes, correct_presses
    labels = "Mistakes", "Correct presses"
    sizes = [mistakes, correct_presses]
    colors = ['red', 'green']
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            startangle=90, colors=colors)
    ax1.axis('equal')
    fig1.set_size_inches(5, 3)
    pie_canvas = FigureCanvasTkAgg(fig1, master=window)
    pie_canvas.get_tk_widget().pack()
    pie_canvas.draw()


def get_duration():
    global end_time, start_time, duration, minutes, seconds
    end_time = pd.datetime.now()
    duration = end_time - start_time
    hours, remainder = divmod(duration.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return "Duration: " + str(minutes) + "min" + " " + str(seconds) + "sec"


def on_key_press(e):
    if (e.keycode != 16):
        global pos, text_widget, b, mistakes, correct_presses, typing_speed
        if (string[pos] != e.char):
            text_widget.tag_add("wrong", str(1) + "." + str(b))
            mistakes += 1
        if (string[pos] == e.char):
            text_widget.tag_add("correct", str(1) + "." + str(b))
            correct_presses += 1
        b += 1
        pos += 1
        if (pos == len(string)):
            draw_pie_chart()
            handle_stats()


def start():
    global start_time
    message.pack()
    text_widget.pack()
    start_btn.destroy()
    start_time = pd.datetime.now()


file = open('text.txt', 'r')
text = file.readlines()
file.close()

string = ""
for i in text:
    for j in range(len(i)):
        string = string + i[j]

window = Tk()
window.wm_title("Keyboard Trainer")

text_widget = Text(window, height=10, width=100,
                   padx=20, pady=20, font=("Arial ", 16))
text_widget.insert(END, string)
text_widget.configure(state="disabled")
text_widget.tag_config("correct", background="green", foreground="white")
text_widget.tag_config("wrong", background="red", foreground="white")


text_widget.bind("<KeyPress>", on_key_press)
text_widget.focus()

message = Label(window,
                text="Start typing",
                font=("Arial ", 24))

start_btn = Button(
    window,
    text="Start",
    width="20",
    height="2",
    padx="1",
    pady="1",
    command=start)

start_btn.pack()

window.mainloop()
