from flask import Flask, render_template, request, redirect, flash
app = Flask(__name__)
from mysqlconnection import connectToMySQL
import os
import re
app.secret_key = os.urandom(16)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/add_email', methods=["POST"])
def add_email_to_db():
    is_valid = True
    if not EMAIL_REGEX.match(request.form['email']):
        is_valid = False
        flash("Invalid email.", "email_format")
    if not is_valid:
        return redirect("/")
    else:
        mysql = connectToMySQL("mydb")
        query = "INSERT INTO emails (email) VALUES (%(em)s);"
        data = {
            'em': request.form["email"]
        }
        mysql.query_db(query, data)
        return redirect("/emails")


@app.route('/emails')
def view_emails():
    # call the function, passing in the name of our db
    mysql = connectToMySQL('mydb')
    # call the query_db function, pass in the query as a string
    emails = mysql.query_db('SELECT * FROM mydb.emails;')
    print(emails)
    return render_template("success.html", all_emails=emails)


if __name__ == "__main__":
    app.run(debug=True)
