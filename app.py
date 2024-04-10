import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
DATABASE = "C:/Users/20245/OneDrive - Wellington College/13DTS/Coding projects/flaskProject2/Dictionary"


def create_connection(db_file):
    #This function creates a connection with the database
    #which means that the database file is open
    #so that cursor objects can be created and used on the open database
    try:
        connection = sqlite3.Connection(db_file)
        return connection
    except Error as e:
        print(e)
    return e

@app.route('/')
def render_home():
    return render_template("home_page.html")

@app.route('/dictionary')
def render_dicionary():
    con = create_connection(DATABASE)
    query = "SELECT word_table.word, word_table.definition"

    return render_template("dictionary_page.html",dictionary=dictionary)


@app.route('/login')
def render_login():
    return render_template("login_page.html")



app.run(host='0.0.0.0', debug=True)