from tkinter import *
import pandas
import random
import pyttsx3

BACKGROUND_COLOR = "#B1DDC6"
to_learn = {}
current_card = {}
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("Japanese_word.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_text, text=current_card["Japanese"], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    global current_card
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")


def is_known():
    to_learn.remove(current_card)
    next_card()
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)


def speak():
    value = canvas.itemcget(card_text, "text")
    voices = engine.getProperty('voices')
    engine.setProperty("voice", voices[2].id)
    engine.setProperty("rate", 150)
    engine.say(value)
    engine.runAndWait()


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Text-to-speech
engine = pyttsx3.init()

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400, 263, text="", font=("Ariel", 60, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=3)

cross_img = PhotoImage(file="wrong.png")
unknown_button = Button(image=cross_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_img = PhotoImage(file="right.png")
known_button = Button(image=check_img, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=2)

speaker_img = PhotoImage(file="megaphone.png")
speaker_button = Button(image=speaker_img, highlightthickness=0, command=speak, bg=BACKGROUND_COLOR)
speaker_button.grid(row=1, column=1)

next_card()

window.mainloop()
