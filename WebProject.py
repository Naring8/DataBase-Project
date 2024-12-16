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
    items = cursor.execute(
        'SELECT Name, Platform, Global_Sales \
        From Games, Sales \
        WHERE Name = gName AND platform = gPlatform').fetchall()
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
            cursor.execute(
                'INSERT INTO Sales (gName, gPlatform)\
                 VALUES (?, ?)',
                (name, platform)
            )
            db.commit()
        except sqlite3.Error as e:
            db.rollback()
            return f"Database error: {e}", 500
        finally:
            db.close()
        return redirect('/ShowGamesInfo/')
    return render_template('NewGamePage.html', platforms = platforms, genres = genres)

@app.route('/UpdateGame/', methods=['GET', 'POST'])
def updateGame():
    game = None
    error = None
    success = None

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'search':
            name = request.form.get('name')
            platform = request.form.get('platform')

            if not name or not platform:
                error = "Error: Game Name and Platform Error"
            else:
                try:
                    db = sqlite3.connect('games.db')
                    cursor = db.cursor()
                    result = cursor.execute(
                        'SELECT Name, Platform, Global_Sales FROM Games, Sales WHERE gName = Name AND gPlatform = Platform AND Name = ? AND Platform = ?',
                        (name, platform)).fetchone()
                    db.close()

                    if result:
                        game = {
                            'name': result[0],
                            'platform': result[1],
                            'sales': result[2]
                        }
                    else:
                        error = "Error: Game not found"
                except sqlite3.Error as e:
                    error = f"Database Error: {e}"

        elif action == 'update':
            # Update the game's sales
            name = request.form.get('name')
            platform = request.form.get('platform')
            new_sales = request.form.get('new_sales')

            if not name or not platform or not new_sales:
                error = "Error: All fields are required to update sales."
            else:
                try:
                    db = sqlite3.connect('games.db')
                    cursor = db.cursor()
                    cursor.execute(
                        'UPDATE Sales SET Global_Sales = ? WHERE gName = ? AND gPlatform = ?',
                        (new_sales, name, platform))

                    if cursor.rowcount == 0:
                        error = "Error: Game not found or no changes made."
                    else:
                        success = "Sales updated successfully!"
                    db.commit()
                except sqlite3.Error as e:
                    db.rollback()
                    error = f"Database error: {e}"
                finally:
                    db.close()
                return redirect('/')

    return render_template('UpdateGamePage.html', game=game, error=error, success=success)

@app.route('/DeleteGame/', methods=['GET', 'POST'])
def deleteGame():
    # Delete Game
    if request.method == 'POST':
        name = request.form.get('name')
        platform = request.form.get('platform')

        if not name or not platform:
            return "Error: Name and Platform are required", 400
        
        try:
            db = sqlite3.connect('games.db')
            cursor = db.cursor()
            cursor.execute(
                'DELETE FROM Games WHERE Name = ? AND Platform = ?',
                (name, platform))
            if cursor.rowcount == 0:
                return "Error: Game not found", 404
            db.commit()
        except sqlite3.Error as e:
            db.rollback()
            return f"Database error: {e}", 500
        finally:
            db.close()
        return redirect('/ShowGamesInfo/')
    
    return render_template('DeleteGamePage.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=7000)