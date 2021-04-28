from flask import Flask, flash, redirect, render_template, request, url_for, session
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/wadlab"
mongo = PyMongo(app)


app.secret_key = 'homework 4'

# login route
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.mycol1
        login_user = users.find_one({'username' : request.form['username']})

        if login_user:
            if request.form['password'] == login_user['password']:
                session['username'] =request.form['username']
                flash('You have logged in successfully')
                return redirect(url_for('home'))
            
        flash('Validation failed')
        return render_template('login.html')
            
              
    return render_template('login.html')


# home route
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

# end session when current user clicks logout button  
@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('login'))


# registration page route
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.mycol1
        existing_user = users.find_one({'username' : request.form['username']})

        if existing_user is None:
            users.insert({'username' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('home'))
            flash('You have registered successfully')
        else:
            flash('Sorry username already exists')

    return render_template('register.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
