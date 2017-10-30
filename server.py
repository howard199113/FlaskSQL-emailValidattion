from flask import Flask, request, redirect, render_template, session, flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'mydb')

app.secret_key = "ThisIsSecret!"


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():

    inputEmails = request.form['email']

    if len(inputEmails) <1:
        flash("Email cannot be blank!")

    elif not EMAIL_REGEX.match(inputEmails):
        flash("Invalid Email Address!")

    elif EMAIL_REGEX.match(inputEmails):
        query = "SELECT email from emails WHERE email = :specific_email"
        data = {'specific_email': inputEmails}
        matchEmail = mysql.query_db(query,data)

        if matchEmail == []:
            query = "INSERT INTO emails(email, created_at, updated_at)VALUES(:email, NOW(), NOW())"
            data = {'email': request.form['email']}
            mysql.query_db(query,data)
            new_query = "SELECT * From emails"
            select = mysql.query_db(new_query)
            return render_template('valid.html', all_emails = select)

        elif matchEmail[0]['email'] == inputEmails:
            flash('Already in DataBase!!!!')
            return redirect('/')
    
    
    
    
    
    
    
    
    
    
    # for x in emails:
    #     if x['email'] == inputEmails:
    #         query = "INSERT INTO emails(email, created_at, updated_at)VALUES(:email, NOW(), NOW())"
    #         data = {'email': request.form['email']}
    #         mysql.query_db(query,data)
    #         allEmails = mysql.query_db("SELECT * FROM emails")
    #         return render_template('/valid.html', validEmail = request.form['email'], all_emails = allEmails)
    # return render_template('index.html', invalid = "Email is Not Valid!")
        
app.run(debug=True)