from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@127.0.0.1/miniproject'
db = SQLAlchemy(app)

class Registration(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(128),nullable = False)
    email = db.Column(db.String(64),nullable = False)
    hashed_password = db.Column(db.String(128),nullable = False)

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

@app.route('/register',methods = ['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        hashed_password = hash_password(password)
        new_registration = Registration(name = name,email = email,hashed_password = hashed_password)

        db.session.add(new_registration)
        db.session.commit()

        flash('Registration is successful')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/')
def index():
    registration = Registration.query.all()
    return render_template('index.html',registration = registration )



if __name__ == '__main__':
    app.run(debug=True)