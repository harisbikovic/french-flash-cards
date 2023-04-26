import tkinter
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Ariel"

common_random_index = 0
to_learn_list = []

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
    to_learn_list = data.to_dict(orient="records")  # With `orient="records"` returns list
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn_list = original_data.to_dict(orient="records")  # With `orient="records"` returns list

def next_card():
    global common_random_index, flip_timer
    common_random_index = random.randint(0, len(to_learn_list)-1)
    window.after_cancel(flip_timer)
    canvas.itemconfig(canvas_image, image=front_img)
    french_word = to_learn_list[common_random_index]["French"]
    canvas.itemconfig(title_on_canvas, text = "French")
    canvas.itemconfig(word_on_canvas, text = french_word)
    flip_timer = window.after(3000, switch_to_english)


def switch_to_english():
    canvas.itemconfig(canvas_image, image=back_img)
    canvas.itemconfig(title_on_canvas, text="English")
    english_word = to_learn_list[common_random_index]["English"]
    canvas.itemconfig(word_on_canvas, text=english_word)


def know_card():
    to_learn_list.remove(to_learn_list[common_random_index])
    next_card()
    data = pandas.DataFrame(to_learn_list)
    data.to_csv("data/words_to_learn.csv", index=False)


window = tkinter.Tk()
window.title("Flash card")
window.config(bg=BACKGROUND_COLOR, pady=50, padx=50)

flip_timer = window.after(3000, switch_to_english)


# Canvas
canvas = tkinter.Canvas(width=800,height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front_img = tkinter.PhotoImage(file="./images/card_front.png")
back_img = tkinter.PhotoImage(file="./images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=front_img)
## Canvas text: 1)Title, 2)Word
title_on_canvas = canvas.create_text(400, 150, text="Title", fill="black", font=(FONT_NAME, 40, "italic"))
word_on_canvas = canvas.create_text(400,263, text="Word", fill="black", font=(FONT_NAME,60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Buttons
wrong_img = tkinter.PhotoImage(file="./images/wrong.png")
right_img = tkinter.PhotoImage(file="./images/right.png")
the_dontknow_button = tkinter.Button(image=wrong_img, command=next_card, highlightthickness=0, border=0)
the_know_button = tkinter.Button(image=right_img, command=know_card, highlightthickness=0, border=0)
the_dontknow_button.grid(column=0, row=1)
the_know_button.grid(column=1, row=1)

next_card()

window.mainloop()