from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Table

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] ='Master_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login_details.db'

db=SQLAlchemy(app)

class Login(db.Model):
    # __tablename__ = 'users'
    email = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(240))

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Entry %r %r>' % (self.email, self.password)

# Create the table
db.create_all()


def authenticate(e, p):
    print(e)
    details=Login.query.filter_by(email=e).filter_by(password=p).all()
    print(details)
    if(len(details)>0):
        return True
    else:
        return False

@app.route('/')
def main():
	 return render_template('login.html')

@app.route('/logout')
def logout():
	session['logged_in'] = False
	session.pop('log_email', None)
	return render_template('login.html',error=None)

@app.route('/login',methods=['GET','POST'])
def login():

    error = None
    if request.method == 'POST':
    	email = request.form['email']
    	psw = request.form['password']
    	if(authenticate(email,psw)):
    		session['logged_in'] = True
    		session['log_email'] = email
    		flash("You are logged in")
    		return redirect(url_for('user'))
    	elif len(Login.query.filter_by(email=email).all())==0:
    		error="User doesn't exist"
    	else:
    		error='Invalid credentials'
    return render_template('login.html', error_l=error)

@app.route('/signup',methods=['GET','POST'])
def signup():

	error = None
	if request.method == 'POST':
		email= request.form['email']
		psw=request.form['password']
		cnf=request.form['cnf_password']
		details=Login.query.filter_by(email=email).all()
		if psw != cnf:
			error = "Passwords do not match"
		elif len(details) != 0:
			error = "User already exists"
		if psw == cnf and len(details)==0:
			print("hel")
			user1=Login(email,psw)
			db.session.add(user1)
			db.session.commit()
			return redirect(url_for('login'))
		else:
			return render_template('login.html', error_s=error)
	else:
		return render_template('login.html', error_s=error)

@app.route('/user')
def user():
	return render_template('user.html')

if __name__ == '__main__':
    app.run()