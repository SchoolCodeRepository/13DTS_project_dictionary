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


def is_logged_in():
    if session.get('email') is None:
        print('not logged in')
        return False
    else:
        print('logged in')
        return True
@app.route('/')
def render_home():
    #This function renders the websites homepage
    return render_template("home_page.html")

@app.route('/dictionary')
def render_dicionary():
    #this function renders the dictionary page, and returns the
    #data from a table to allow the site to acess it using sql
    con = create_connection(DATABASE)
    query = '''SELECT word_table.word, word_table.definition, word_table.level, word_table.english_translation, word_table.category, users_table.user_id
                FROM word_table INNER JOIN users_table ON word_table.user_id_fk = users_table.user_id'''
    cur = con.cursor()
    cur.execute(query)
    word_list = cur.fetchall()
    print(word_list)
    con.close()
    return render_template("dictionary_page.html",word_list=word_list)


@app.route('/login', methods=['POST','GET'])
def render_login():
    if is_logged_in():
        return redirect('/')
    print('logging in')
    #this function renders the dictionary page of the website
    if request.method == 'POST':
        #This gets the signin information from the user and checks to see if they are in the database.
        email = request.form.get('email')
        password_input = request.form.get('password')
        print(email)
        con = create_connection(DATABASE)
        query = """SELECT *  
                    FROM users_table WHERE email = ?"""
        cur = con.cursor()
        cur.execute(query, (email,))
        user_info = cur.fetchall()
        con.close()
        print(user_info)
        try:
            user_id = user_info[0]
            user_fname = user_info[1]
            user_lname = user_info[2]
            user_perms = user_info[3]
            user_password = user_info[4]
            user_email = user_inf[5]
        except IndexError:
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
        if password != confirm_password:
            return redirect('/register?error=passwords+do+not+match')
        elif len(password) < 10:
            return redirect('/register?error=password+not+long+enough')
        else:
            con  = create_connection(DATABASE)
            try:
                cur = con.cursor()
                # This sql adds the new users information to the database
                query_users = "INSERT INTO users_table(fname, lname, permissions, password, email) VALUES(?,?,?,?,?)"
                cur.execute(query_users, (fname, lname, permisson, password, email))
            except sqlite3.IntegrityError:
                con.close()
                return redirect('/register?email+already+in+use')
            con.commit()
            con.close()
            return redirect('/login')
    return render_template("register_page.html")

app.run(host='0.0.0.0', debug=True)