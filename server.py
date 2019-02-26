from flask import Flask, render_template, request, redirect, session
# import the function that will return an instance of a connectioncopy
from mysqlconnection import connectToMySQL
import random
import time    


# Justin just added this comment
# Now this

app = Flask(__name__)
app.secret_key = "shh"


def board_create():
    def color_gen():
        done = False
        color_list = []
        brown_count = 5
        red_count = 5
        blue_count = 5
        black_count = 1

        while not done:
            num = random.randint(1, 4)
            if num == 1 and brown_count > 0:
                color_list.append("brown")
                brown_count -= 1
            if num == 2 and red_count > 0:
                color_list.append("red")
                red_count -= 1
            if num == 3 and blue_count > 0:
                color_list.append("blue")
                blue_count -= 1
            if num == 4 and black_count > 0:
                color_list.append("black")
                black_count -= 1
            if black_count == 0 and red_count == 0 and brown_count == 0 and blue_count == 0:
                done = True

        print(color_list)
        print(len(color_list))
        return color_list


    reg_bank = ['hello', 'trumpet', 'ladybug', 'sponge', 'China', 'cupcake', 'jungle',
                'soccer', 'spatula', 'crown', 'farmer', 'clock', 'monster', 'flag', 'garbage', 'pencil']
    color_list = color_gen()

    colored_bank = []
    for i in range(16):
        colored_bank.append({'word': reg_bank[i], 'color': color_list[i]})
    
    return colored_bank



@app.route("/")
def index():
    return render_template("index.html")


@app.route('/reset')
def reset():

    if 'game_id' in session:
        data = {
            'game_id' : session['game_id']
        }

        mysql = connectToMySQL('codenames_db')
        query = "DELETE FROM cards WHERE game_id = %(game_id)s;"
        game_delete = mysql.query_db(query, data)
        print(game_delete, "did it delete?")


    data = {
        'card_info' : board_create()
    }
    session['bank'] = data['card_info']

    game_id = time.strftime('%Y-%m-%d %H:%M:%S')
    for card in data['card_info']:

        data= {
            'color' : card['color']
        }

        mysql = connectToMySQL('codenames_db')
        query = "INSERT INTO colors (color) VALUES (%(color)s);"
        color_id = mysql.query_db(query, data)

        data= {
            'word' : card['word']
        }

        mysql = connectToMySQL('codenames_db')
        query = "INSERT INTO words (word) VALUES (%(word)s);"
        word_id = mysql.query_db(query, data)


        data= {
            'color_id' : color_id,
            'word_id' : word_id,
            'game_id' : game_id
        }

        mysql = connectToMySQL('codenames_db')
        query = "INSERT INTO cards (color_id, word_id, game_id) VALUES (%(color_id)s, %(word_id)s, %(game_id)s);"
        card_id = mysql.query_db(query, data)

    session['game_id'] = game_id

    return redirect('/gameboard')

@app.route('/spymaster', methods = ['POST', 'GET'])
def secret():

    if request.method == 'POST':

        data = {
            'game_key' : request.form['game_key']
        }

        mysql = connectToMySQL('codenames_db')
        query = "SELECT colors.color AS 'color', words.word AS 'word' FROM cards JOIN colors ON colors.id = cards.color_id JOIN words ON words.id = cards.word_id WHERE game_id = %(game_key)s;"
        game_info =  mysql.query_db(query, data)
        print(game_info)
        print('VS')
        # print(session['bank'])

        try:
            print(game_info[0]) #testing if anything is inside "game_info", in otherwords, was the query successful
            if 'bank' not in session:
                session['bank'] = game_info
            
            return redirect('/secret')
        except:
            return redirect('/spymaster')
    else:
        return render_template('/spymaster.html')

@app.route('/gameboard')
def gameboard():
    return render_template('gameboard.html', bank=session['bank'])

@app.route('/secret')
def spyboard():
    return render_template('secret.html', bank = session['bank'])

# @app.route("/party_create", methods = ['POST'])
# def party_create():
#     party_data_SQL = connectToMySQL('party_game_db')
#     query =
#     party_data = party_data_SQL.query_db(query, data)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port = 6969)
