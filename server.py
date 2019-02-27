from math import floor
from random import randint, random
from flask import Flask, render_template, request, redirect, session, flash
# import the function that will return an instance of a connectioncopy
from mysqlconnection import connectToMySQL
import time
from wordbank import word_bank

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
        arr[i], arr[amnt_to_shuffle] = arr[amnt_to_shuffle].upper(), arr[i]
    print(arr)
    return arr


# create and shuffle board
def board_create():

    card_bank = ["red", "red", "red", "red", "red", "blue", "blue", "blue",
                 "blue", "blue", "brown", "brown", "brown", "brown", "brown", "black"]

    # clear gameboard
    colored_bank = []

    # shuffle card_bank
    color_list = shuffle(card_bank)
    shuffled_words = shuffle(word_bank)

    # append shuffled card_bank to colored_bank
    for i in range(16):
        colored_bank.append(
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

# GET "/reset"
@app.route('/reset')
def reset():

    if 'game_id' in session:
        data = {
            'game_id': session['game_id']
        }

        mysql = connectToMySQL('codenames_db')
        query = "DELETE FROM cards WHERE game_id = %(game_id)s;"
        game_delete = mysql.query_db(query, data)
        print(game_delete, "did it delete?")

    data = {
        'card_info': board_create()
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

    return redirect('/gameboard')


@app.route('/spymaster', methods=['POST', 'GET'])
def secret():
    # POST "/spymaster"
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
            return redirect('/spymaster')
    # GET "/spymaster"
    else:
        return render_template('/spymaster.html')

# GET "/gameboard"
@app.route('/gameboard')
def gameboard():
    if 'bank' not in session:
        return redirect('/reset')
    return render_template('gameboard.html', bank=session['bank'])

# GET "/secret"
@app.route('/secret')
def spyboard():
    if 'bank' not in session:
        return redirect('/spymaster')
    return render_template('secret.html', bank=session['bank'])


if __name__ == "__main__":
    app.run(debug=True)
