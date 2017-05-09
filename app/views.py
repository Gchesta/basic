from datetime import date
from flask import render_template, url_for, request, redirect, url_for, flash, abort
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from app import app
from . import forms #LoginForm, SignupForm
from .models import Project, User, engine
import werkzeug.security as ws
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
import csv
import io

login_manager = LoginManager()
login_manager.init_app(app)

DBSession = sessionmaker(bind=engine)
dbsession = DBSession()

@login_manager.user_loader
def load_user(id):
    return dbsession.query(User).filter_by(id=id).first()

"""@app.route("/signup.html", methods=["GET", "POST"])
def signup():
    form = forms.SignupForm()
    if form.is_submitted:
        user = User(
        username = form.username.data,
        pwhash= ws.generate_password_hash(form.password.data)
        )
        dbsession.add(user)
        dbsession.commit()
        return redirect("/new-projects.html")
    return render_template("signup.html", form=form)"""

@app.route("/login.html", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = dbsession.query(User).filter_by(username=form.username.data).first()
        if ws.check_password_hash(user.pwhash, form.password.data):
            login_user(user)
            return redirect("/new-projects.html")
    return render_template("login.html", form=form)

@app.route("/", methods=["GET", "POST"])
def view_results():
    select_form = forms.SelectSubjectForm()
    if select_form.subject_submit.data:
        all_projects = dbsession.query(Project).filter_by(subject=select_form.subject.data).all()
        presented_projects = [project for project in all_projects if project.score]
        projects = sorted(presented_projects, key=lambda project: project.score, reverse=True)
        length = len(projects)
        try:
            projects[0].rank = 1
            projects[0].count = 1
        except Exception:
            pass
        for position in range(1, length):
            if projects[position].score == projects[position - 1].score:
                projects[position].rank = projects[position - 1].rank
            else:
                projects[position].rank = position + 1
            projects[position].count = position + 1
        return render_template("view-results.html", select_form=select_form, projects=projects)
    return render_template("view-results.html", select_form=select_form)

@app.route("/new-projects.html", methods=["GET", "POST"])
@login_required
def new_projects():
    file_form = forms.ProjectFileForm()
    if file_form.file.data:
        file_data = request.files["file"]
        stream = io.StringIO(file_data.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.reader(stream)
        #print(csv_input)
        subject = file_form.subject.data
        for row in csv_input:
            new_project = Project(
            school=row[0],
            zone = row[1],
            first_presenter = row[2],
            second_presenter = row[3],
            title = row[4],
            subject=subject
            )
            dbsession.add(new_project)
        dbsession.commit()
    return render_template("projects.html", file_form=file_form)

@app.route("/add-scores.html", methods=["GET", "POST"])
@login_required
def add_scores():
    form = forms.AddScoresForm()
    select_form = forms.SelectSubjectForm()
    if form.score_submit.data:
        project = dbsession.query(Project).filter_by(project_id=form.project_id.data).first()
        project.score = form.score.data
        dbsession.commit()
        all_projects = dbsession.query(Project).filter_by(subject=project.subject).all()
        projects = [project for project in all_projects if not project.score]
        length = len(projects)
        try:
            projects[0].count = 1
        except:
            pass
        for count in range(1, length):
            projects[count].count = count + 1
        return render_template("add-scores.html", select_form=select_form, form=form, projects=projects)
    elif select_form.subject_submit.data:
        all_projects = dbsession.query(Project).filter_by(subject=select_form.subject.data).all()
        projects = [project for project in all_projects if not project.score]
        length = len(projects)
        try:
            projects[0].count = 1
        except:
            pass
        for count in range(1, length):
            projects[count].count = count + 1
        return render_template("add-scores.html", select_form=select_form, form=form, projects=projects)
    return render_template("add-scores.html", form=form, select_form=select_form)
