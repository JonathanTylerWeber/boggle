from flask import Flask, request, render_template, redirect, session
from boggle import Boggle
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def index():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('index.html', board=board)

