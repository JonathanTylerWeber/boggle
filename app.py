from flask import Flask, request, render_template, redirect, session, jsonify
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def start_page():
    """create start page"""
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template('start.html', highscore=highscore, nplays=nplays)

@app.route('/game')
def index():
    """create game board and start game"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template("index.html", board=board, highscore=highscore, nplays=nplays)

@app.route('/endgame', methods=['GET', 'POST'])
def end_game():
    """end game saving number of plays and updating high score"""
    session['nplays'] = session.get('nplays', 0) + 1
    score = session.pop('score', 0)
    highscore = session.get('highscore', 0)
    if score > highscore:
        session['highscore'] = score
    print("nplays:", session['nplays'])
    return redirect('/')

@app.route('/guess', methods=['GET', 'POST'])
def guess():
    """check if guess is valid word and on board, update session score"""
    user_guess = request.json.get('guess')
    with open('words.txt', 'r') as file:
        for line in file:
            if line.strip() == user_guess:
                result = boggle_game.check_valid_word(session['board'], user_guess)
                if result == 'ok':
                    score = session.get('score', 0)
                    score += len(user_guess)
                    session['score'] = score
                    return jsonify(result='ok', message='Word is valid and exists on the board.')
                elif result == 'not-on-board':
                    return jsonify(result='not-on-board', message='Word is not on the board.')
    return jsonify(result='not-word', message='Word is not a valid word.')