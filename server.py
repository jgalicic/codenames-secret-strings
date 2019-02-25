from flask import Flask, render_template, request, redirect, session
# import the function that will return an instance of a connectioncopy
from mysqlconnection import connectToMySQL
import random

# Justin just added this comment
# Now this

app = Flask(__name__)
app.secret_key = "shh"


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


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/gameboard')
def gameboard():
    return render_template('gameboard.html', bank=colored_bank)

# @app.route("/party_create", methods = ['POST'])
# def party_create():
#     party_data_SQL = connectToMySQL('party_game_db')
#     query =
#     party_data = party_data_SQL.query_db(query, data)


if __name__ == "__main__":
    app.run(debug=True)
