from math import floor
from random import randint, random
from flask import Flask, render_template, request, redirect, session, flash
# import the function that will return an instance of a connectioncopy
from mysqlconnection import connectToMySQL
import time
from wordbank import word_bank
from lovebank import love_bank

app = Flask(__name__)
app.secret_key = "shh"

####################################
########### Functions ##############
####################################


def shuffle(arr):
    amnt_to_shuffle = len(arr)
    while amnt_to_shuffle > 1:
        i = int(floor(random() * amnt_to_shuffle))
        amnt_to_shuffle -= 1
        arr[i], arr[amnt_to_shuffle] = arr[amnt_to_shuffle], arr[i]
    return arr


# create and shuffle board
def board_create(bank_id):

    card_bank = ["red", "red", "red", "red", "red", "blue", "blue", "blue",
                 "blue", "blue", "brown", "brown", "brown", "brown", "brown", "black"]

    # clear gameboard
    colored_bank = []

    # shuffle card_bank
    color_list = shuffle(card_bank)

    # decide which word bank to use
    if bank_id == 1:
        shuffled_words = shuffle(word_bank)
        session['bank_id'] = 1
    if bank_id == 2:
        shuffled_words = shuffle(love_bank)
        session['bank_id'] = 2

    # append shuffled card_bank to colored_bank
    for i in range(16):
        colored_bank.append(
            # change line below to shuffled_words1[i] or shuffled_words2[i]
            {'word': shuffled_words[i], 'color': color_list[i]})

    return colored_bank

# generate friendly key function


def friendly_key_gen():

    keycodebank = [['S', 'T', 'U', 'V', 'W', 'X', 'Y'],
                   ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                   ['2', '3', '4', '5', '6', '7', '8'],
                   ['J', 'K', 'L', 'M', 'N', 'P', 'Q']]

    alpha_code = ''

    for x in keycodebank:
        randomdigit = int(floor(random() * len(x)))
        alpha_code += x[randomdigit]

    return alpha_code

####################################
############# Routes ###############
####################################


# GET "/"
# Landing page
@app.route("/")
def index():
    return render_template("index.html")

# GET "/instructions"
@app.route('/instructions')
def instructions():

    return render_template('instructions.html')

# GET "/setup/1"
# Instructions for spymasters
@app.route("/setup/1")
def setup1():
    return render_template("setup1.html")

# GET "/setup/2"
# Randomly displays which team will start
@app.route("/setup/2")
def setup2():
    side_to_start = int(floor(random() * 2))
    return render_template("setup2.html", side_to_start=side_to_start)

# GET "/reset/<bank_id>"
@app.route('/reset/<bank_id>')
def reset(bank_id):

  # The TRUNCATE queries below remove all table information each time the game starts.
  # This may cause problems when multiple games are played at the same time.

    # remove previous entries from database
    mysql = connectToMySQL('codenames_db')
    query = "TRUNCATE TABLE words;"
    db_delete_words = mysql.query_db(query)  # this is required

    mysql = connectToMySQL('codenames_db')
    query = "TRUNCATE TABLE colors;"
    db_delete_colors = mysql.query_db(query)  # this is required

    mysql = connectToMySQL('codenames_db')
    query = "TRUNCATE TABLE cards;"
    db_delete_cards = mysql.query_db(query)  # this is required

    data = {
        'card_info': board_create(int(bank_id))
    }
    session['bank'] = data['card_info']

    game_id = time.strftime('%Y-%m-%d %H:%M:%S')

    friendly_key = friendly_key_gen()

    for card in data['card_info']:

        data = {
            'color': card['color']
        }

        mysql = connectToMySQL('codenames_db')
        query = "INSERT INTO colors (color) VALUES (%(color)s);"

        # database call
        color_id = mysql.query_db(query, data)

        data = {
            'word': card['word']
        }

        mysql = connectToMySQL('codenames_db')
        query = "INSERT INTO words (word) VALUES (%(word)s);"
        word_id = mysql.query_db(query, data)

        data = {
            'color_id': color_id,
            'word_id': word_id,
            'game_id': game_id,
            'friendly_key': friendly_key
        }

        mysql = connectToMySQL('codenames_db')
        query = ("INSERT INTO cards (color_id, word_id, game_id, friendly_key) "
                 "VALUES (%(color_id)s, %(word_id)s, %(game_id)s, %(friendly_key)s); ")
        card_id = mysql.query_db(query, data)  # this is required

    session['game_id'] = game_id
    session['friendly_key'] = friendly_key

    return redirect('/setup/1')


@app.route('/spy', methods=['POST', 'GET'])
def secret():
    # POST "/spy"
    if request.method == 'POST':

        data = {
            'game_key': request.form['game_key']
        }

        mysql = connectToMySQL('codenames_db')
        query = ("SELECT colors.color AS 'color', words.word AS 'word' "
                 "FROM cards JOIN colors ON colors.id = cards.color_id "
                 "JOIN words ON words.id = cards.word_id "
                 "WHERE friendly_key = %(game_key)s; ")
        game_info = mysql.query_db(query, data)

        try:
            # testing if anything is inside "game_info", in otherwords, was the query successful
            print(game_info[0])
            session['bank'] = game_info

            return redirect('/secret')
        except:
            flash("Error: Incorrect Spymaster key", "spy_error")
            return redirect('/spy')
    # GET "/spymaster"
    else:
        return render_template('/spymaster.html')

# GET "/gameboard/<color_id>"
@app.route('/gameboard/<color_id>')
def gameboard(color_id):
    if 'bank' not in session:
        return redirect('/reset')
    return render_template('gameboard.html', bank=session['bank'], color_id=int(color_id))

# GET "/secret"
@app.route('/secret')
def spyboard():
    if 'bank' not in session:
        return redirect('/spy')
    return render_template('secret.html', bank=session['bank'])


@app.route('/win/<team>')
def win(team):
    return render_template('win.html', team=team)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
