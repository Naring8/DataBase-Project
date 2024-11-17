from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def mainPage():
    # Main Web Page
    return render_template('MainPage.html')

@app.route('/ShowGamesInfo/')
def showGamesInfo():
    # connect to Games DB
    return render_template('GamesInfo.html')

@app.route('/InsertNewGame/')
def newGame():
    # Enroll New Game
    return render_template('NewGamePage.html')

@app.route('/UpdateGame/')
def updateGame():
    # Update Game
    return render_template('UpdateGamePage.html')

@app.route('/DeleteGame/')
def deleteGame():
    # Delete Game
    return render_template('DeleteGamePage.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=7000)