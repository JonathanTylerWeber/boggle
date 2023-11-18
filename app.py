from flask import Flask, request, render_template, redirect, session, jsonify
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def start_page():
    return render_template('start.html')

@app.route('/game')
def index():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    user_guess = request.json.get('guess')
    with open('words.txt', 'r') as file:
        for line in file:
            if line.strip() == user_guess:
                result = boggle_game.check_valid_word(session['board'], user_guess)
                if result == 'ok':
                    return jsonify(result='ok', message='Word is valid and exists on the board.')
                elif result == 'not-on-board':
                    return jsonify(result='not-on-board', message='Word is not on the board.')
    return jsonify(result='not-word', message='Word is not a valid word.')