from math import floor
from random import randint, random
from flask import Flask, render_template, request, redirect, session
# import the function that will return an instance of a connectioncopy
from mysqlconnection import connectToMySQL
# import random

# Justin just added this comment
# Now this

app = Flask(__name__)
app.secret_key = "shh"


card_bank = ["red", "red", "red", "red", "red", "blue", "blue", "blue",
             "blue", "blue", "brown", "brown", "brown", "brown", "brown", "black"]

word_bank = ['hello', 'trumpet', 'ladybug', 'sponge', 'China', 'cupcake', 'jungle',
             'soccer', 'spatula', 'crown', 'farmer', 'clock', 'monster', 'flag', 'garbage', 'pencil']

# shuffle function


def shuffle(arr):
    amnt_to_shuffle = len(arr)
    while amnt_to_shuffle > 1:
        i = int(floor(random() * amnt_to_shuffle))
        amnt_to_shuffle -= 1
        arr[i], arr[amnt_to_shuffle] = arr[amnt_to_shuffle], arr[i]
    print(arr)
    return arr


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/gameboard')
def gameboard():

    # clear gameboard
    colored_bank = []

    # shuffle card_bank
    color_list = shuffle(card_bank)

    # append shuffled card_bank to colored_bank
    for i in range(16):
        colored_bank.append({'word': word_bank[i], 'color': color_list[i]})
    return render_template('gameboard.html', bank=colored_bank)


if __name__ == "__main__":
    app.run(debug=True)
