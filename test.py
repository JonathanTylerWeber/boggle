from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont_show_debug_toolbar']


class FlaskTests(TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['SECRET_KEY'] = 'secret'
        with self.client.session_transaction() as session:
            session['highscore'] = 0
            session['nplays'] = 0
            session.update()

    def test_start_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="start" id="start-title">Boggle</h1>', html)
            with self.client.session_transaction() as session:
                self.assertEqual(session['highscore'], 0)
                self.assertEqual(session['nplays'], 0)

    def test_game_page(self):
        with app.test_client() as client:
            res = client.get('/game')
            self.assertEqual(res.status_code, 200)
            with self.client.session_transaction() as session:
                session['board'] = res.data.decode('utf-8')
                self.assertIn('board', session)
                board = session['board']
                self.assertIsNotNone(board)
                self.assertEqual(session['highscore'], 0)
                self.assertEqual(session['nplays'], 0)
            html = res.get_data(as_text=True)
            self.assertIn('<div id="game-board">', html)

    def test_endgame(self):
        with self.client as client:
            with client.session_transaction() as session:
                session['score'] = 10

            res = client.post('/endgame')
            with client.session_transaction() as session:
                self.assertEqual(session['nplays'], 1)
                self.assertEqual(session['highscore'], 10)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')

    def test_endgame_redirect(self):
        with app.test_client() as client:
            res = client.get('/endgame', follow_redirects=True)
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h1 class="start" id="start-title">Boggle</h1>', html)

                
    