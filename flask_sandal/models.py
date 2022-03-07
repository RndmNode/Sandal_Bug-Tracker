from datetime import datetime
from email.policy import default
from flask_sandal import db

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
    description = db.Column(db.String(60), nullable=False)
    priority = db.Column(db.String(15), nullable=False)
    details = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # states and their progression levels in order: ['New', 'Open', 'Pending', 'Resolved', 'Closed']
    state = db.Column(db.Text, nullable=False, default='New')

    # relationships
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"Issue('{self.ticket_number}, {self.description}, {self.priority}, {self.date_posted}, {self.details}')"

class Update(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.Column(db.Text, nullable=False, default="")

    # relationships
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.ticket_number'), nullable=False)

    def __repr__(self):
        return f"Update('{self.id}, {self.details}, {self.date_posted}')"