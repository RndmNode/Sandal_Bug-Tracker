from select import select
from flask import render_template, url_for, flash, redirect, request, abort
from flask_sandal import app, db, crypt
from flask_sandal.models import User, Project, Issue, Update, user_project
from flask_sandal.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewProjectForm
from flask_login import login_user, current_user, logout_user, login_required 

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and crypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = crypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created. You are now able to login.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Signup', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    projects_query = db.session.query(user_project).filter(user_project.c.user==current_user.username)
    user_projects = [i.project for i in db.session.execute(projects_query).all()]
    projects = Project.query.filter(Project.name.in_(user_projects)).all()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form, projects=projects)

@app.route('/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = NewProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, admin=current_user.username)
        user = User.query.filter_by(username=current_user.username).first()
        user.projects.append(project)
        db.session.add(project)
        db.session.commit()
        flash(f'Project has been created.', 'success')
        return redirect(url_for('account'))
    return render_template('create_project.html', title='New Project', form=form)

@app.route('/projects')
@login_required
def projects():
    projects_query = db.session.query(user_project).filter(user_project.c.user==current_user.username)
    user_projects = [i.project for i in db.session.execute(projects_query).all()]
    projects = Project.query.filter(Project.name.in_(user_projects)).all()
    return render_template('projects.html', title='Projects', projects=projects)

@app.route('/projects/<project_id>')
@login_required
def project(project_id):
    project = Project.query.get_or_404(project_id)
    for teammate in project.team:
        if teammate.username == current_user.username:
            return render_template('project.html', title=project.name, project=project)
    flash(f'You need to be added to this project in order to access its page.', 'danger')
    return redirect(url_for('account'))

@app.route('/projects/<project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if current_user.username != project.admin:
        abort(403)
    print("deleting project", project.name)
    # delete all updates for issues on projects
    # delete all issues on projects
    # delete all links to people and projects in user_project
    db.session.delete(project)
    db.session.commit()
    flash(f'Project has been deleted.', 'success')
    return redirect(url_for('account'))