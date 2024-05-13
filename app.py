import sqlite3
from sqlite3 import Error
from flask import Flask, render_template, redirect, request, session

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
    #This function renders the websites homepage
    return render_template("home_page.html")

@app.route('/dictionary')
def render_dicionary():
    #this function renders the dictionary page, and returns the
    #data from a table to allow the site to acess it using sql
    con = create_connection(DATABASE)
    query = '''SELECT word_table.word, word_table.definition, word_table.level, word_table.english_translation, word_table.category 
                FROM collation INNER JOIN word_table ON collation.word_id_fk = word_table.word_id'''
    cur = con.cursor()
    cur.execute(query)
    word_list = cur.fetchall()
    print(word_list)
    con.close()
    return render_template("dictionary_page.html",word_list=word_list)


@app.route('/login', methods=['POST','GET'])
def render_login():
    #this function renders the dictionary page of the website
    if request.method == 'POST':
        #This gets the signin information from the user and checks to see if they are in the database.
        email = request.form.get('email')
        con = create_connection(DATABASE)
        cur = con.cursor()
        query = """SELECT user_id.user_table, email.users_table, password.users_table  
                    FROM collation INNER JOIN users_table ON collation.users_id_fk = users_table.user_id
                    WHERE email.users_table = ?"""
        cur.execute(query, (email,))
        user_info = cur.fetchall()
        con.close()
        print(user_info)
    return render_template("login_page.html")

@app.route('/register', methods=['POST','GET'])
def render_register():
    email_test=[]
    #this function renders the registration page on the website, and collects the users data.
    if request.method == 'POST':
        #this if statement collects data from the registration form, and then tests to see if its appropriate
        #before inserting it into the database
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        permisson = request.form.get('permisson')
        print(f'{fname} {lname} {password} {confirm_password} {email} {permisson} ')
        #this set of conditions makes sure that the signup details reach certain specifications
        for character in email:
            email_test.append(character)
        if password != confirm_password:
            return redirect('/register?error=passwords+do+not+match')
        elif len(password) < 10:
            return redirect('/register?error=password+not+long+enough')
        elif '@' not in email_test:
            return redirect('/register?error=invalid+email')
        else:
            con  = create_connection(DATABASE)
            #This sql adds the new users information to the database
            query = "INSERT INTO users_table(fname, lname, permissions, password, email) VALUES(?,?,?,?,?)"
            try:
                cur = con.cursor()
                cur.execute(query, (fname, lname, permisson, password, email))
            except sqlite3.IntegrityError:
                con.close()
                return redirect('/register?email+already+in+use')
            con.commit()
            con.close()
            return redirect('/login')
    return render_template("register_page.html")

app.run(host='0.0.0.0', debug=True)