from flask import Flask
import sqlite3 as sql

DB_PATH = "distribuidas.db"

def create_db():
    conn = sql.connect('database.db')
    print("Opened database successfully")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    create_db()
    app.run(port=8082)