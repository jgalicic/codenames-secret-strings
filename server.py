from math import floor
from random import randint, random
from flask import Flask, render_template, request, redirect, session, flash
# import the function that will return an instance of a connectioncopy
from mysqlconnection import connectToMySQL
import time
from wordbank import word_bank
from lovebank import love_bank


# Justin just added this comment
# Now this

app = Flask(__name__)
app.secret_key = "shh"

####################################
########### Functions ##############
####################################

# shuffle function


def shuffle(arr):
    amnt_to_shuffle = len(arr)
    while amnt_to_shuffle > 1:
        i = int(floor(random() * amnt_to_shuffle))
        amnt_to_shuffle -= 1
        arr[i], arr[amnt_to_shuffle] = arr[amnt_to_shuffle], arr[i]
    print(arr)
    return arr


# create and shuffle board
def board_create(bank_id):

    card_bank = ["red", "red", "red", "red", "red", "blue", "blue", "blue",
                 "blue", "blue", "brown", "brown", "brown", "brown", "brown", "black"]

    # clear gameboard
    colored_bank = []
    colored_bank2 = []

    # shuffle card_bank
    color_list = shuffle(card_bank)

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

# Generate friendly key function


def friendly_key_gen(ugly_key):

    alpha = ['c', 'o', 'd', 'e', 'n', 'a', 'm', 'x', 's', '-']

    code = ugly_key.replace(' ', '').replace('-', '').replace(':', '')
    alpha_code = ''

    for i in range(6, len(code)):
        num = int(code[i])
        alpha_code += alpha[num]

    return alpha_code

####################################
############# Routes ###############
####################################


# GET "/"
@app.route("/")
def index():
    return render_template("index.html")

# GET "/setup/1"
@app.route("/setup/1")
def setup1():
    return render_template("setup1.html")

# GET "/setup/2"
@app.route("/setup/2")
def setup2():
    side_to_start = int(floor(random() * 2))
    return render_template("setup2.html", side_to_start=side_to_start)

# GET "/reset/<bank_id>"
@app.route('/reset/<bank_id>')
def reset(bank_id):

    if 'game_id' in session:
        data = {
            'game_id': session['game_id']
        }

        mysql = connectToMySQL('codenames_db')
        query = "DELETE FROM cards WHERE game_id = %(game_id)s;"
        game_delete = mysql.query_db(query, data)
        print(game_delete, "did it delete?")

    data = {
        'card_info': board_create(int(bank_id))
    }
    session['bank'] = data['card_info']

    game_id = time.strftime('%Y-%m-%d %H:%M:%S')

    friendly_key = friendly_key_gen(game_id)
    print(friendly_key)

    for card in data['card_info']:

        data = {
            'color': card['color']
        }

        mysql = connectToMySQL('codenames_db')
        query = "INSERT INTO colors (color) VALUES (%(color)s);"
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
        query = "INSERT INTO cards (color_id, word_id, game_id, friendly_key) VALUES (%(color_id)s, %(word_id)s, %(game_id)s, %(friendly_key)s);"
        card_id = mysql.query_db(query, data)

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
        query = "SELECT colors.color AS 'color', words.word AS 'word' FROM cards JOIN colors ON colors.id = cards.color_id JOIN words ON words.id = cards.word_id WHERE friendly_key = %(game_key)s;"
        game_info = mysql.query_db(query, data)
        print(game_info)
        print('VS')
        # print(session['bank'])

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

# GET "/instructions"
@app.route('/instructions')
def instructions():

    return render_template('instructions.html')


@app.route('/win/<team>')
def win(team):
    return render_template('win.html', team=team)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
