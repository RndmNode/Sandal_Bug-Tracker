from crypt import methods
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ef3ef11521a594a6bb4573fb466ba31f'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

user_project = db.Table('user_project',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

class User(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # relationships
    projects = db.relationship('Project', secondary=user_project, backref='team')

    def __repr__(self):
        return f"User('{self.username}, {self.email}')"

class Project(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    # relationships
    issues = db.relationship('Issue', backref='project', lazy=True)

    def __repr__(self):
        return f"Project('{self.name}, {self.id}')"

class Issue(db.Model):
    # columns
    ticket_number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False)
    priority = db.Column(db.String(15), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=False)
    # relationships
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"Issue('{self.ticket_number}, {self.title}, {self.priority}, {self.date_posted}, {self.details}')"

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'tz@g.com' and form.password.data == 'haha':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
        
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html', form=form)

def run():
    app.run(debug=True, port='8000')

if __name__ == "__main__":
    run()