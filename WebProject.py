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
    db = sqlite3.connect('games.db')
    cursor = db.cursor()
    items = cursor.execute('SELECT Name From Games').fetchall()
    db.close()
    return render_template('GamesInfo.html', games=items)

@app.route('/InsertNewGame/', methods=['GET', 'POST'])
def newGame():
    # Enroll New Game
    platforms = ['3DS','PC', 'PS4', 'PS5', 'Switch', 'X360', 'XOne']
    genres = ['Action', 'Adventure', 'Fighting', 'Misc', 'Platform', 'Puzzle', 'Racing', 'Role-Playing', 'Shooter', 'Simulation', 'Sports', 'Strategy']
    if request.method == 'POST':
        name = request.form.get('name')
        platform = request.form.get('platform')
        year = request.form.get('year')
        genre = request.form.get('genre')
        publisher = request.form.get('publisher')

        if not name or not platform:
            return "Error: Check name and platform input", 400
        
        try:
            db = sqlite3.connect('games.db')
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO Games (Name, Platform, Year, Genre, Publisher) VALUES (?, ?, ?, ?, ?)', 
                (name, platform, year, genre, publisher))
            db.commit()
        except sqlite3.Error as e:
            db.rollback()
            return f"Databas error: {e}", 500
        finally:
            db.close()
        return redirect('/ShowGamesInfo/')
    return render_template('NewGamePage.html', platforms = platforms, genres = genres)

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