# GroundScratch main python file with so many yeets that i can't count
from flask import Flask, render_template, request, session, redirect, url_for, jsonify, flash, send_from_directory
from werkzeug.utils import secure_filename
import os
import random
import string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from flask_cors import CORS
import textwrap
from settings import *
from flask_migrate import Migrate

db = SQLAlchemy()

def random_filename(length):
    # With combination of lower and upper case
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    # return random string (some shitty site gave me this function but only a print not a return lol)
    return result_str


app = Flask('GroundScratch')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['ROOT_URL'] = ROOT_URL
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})
migrate = Migrate(app, db)
migrate.init_app(app, db)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    realid = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(1000), unique=True)
    description = db.Column(db.String(5000))
    avatar_file = db.Column(db.String(85))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    project_file = db.Column(db.String(80), unique=True)
    authorid = db.Column(db.Integer)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

app.register_error_handler(404, page_not_found)

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

app.register_error_handler(500, server_error)

login_manager = LoginManager()
login_manager.login_view = 'login_page'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
  # since the user_id is just the primary key of our user table, use it in the query for the user
  return User.query.get(int(user_id))


@app.before_request 
def before_request_callback(): 
  if current_user.is_authenticated:
    user = User.query.get(current_user.id)
    if user.realid == None:
      user.realid = random_filename(64)
      db.session.merge(user)
      db.session.commit()
    if user.description == None:
      user.description = "Hi! I'm a new user on GroundScratch, but I haven't a description yet... :3"
      db.session.merge(user)
      db.session.commit()

@app.route('/')
def home():
  if current_user.is_authenticated:
    return render_template('index.html', username=current_user.name)
  else:
    return render_template("index.html")
  
@app.route('/project/<int:project_number>/')
def project_page(project_number):
  project = Project.query.filter_by(id=project_number).first()
  if project:
    user = User.query.filter_by(id=project.authorid).first()
    return render_template('project.html', project_number=project_number, url_for_project=app.config['ROOT_URL'] + "project_file/" + project.project_file, project=project, authorname=user.name)
  else:
        return render_template('project-404.html', project_number=project_number)

@app.route('/create/', methods=['GET', 'POST'])
@login_required
def createproject_page():
  if request.method == 'POST':
    file = request.files['file']
    if not file.filename.endswith(".sb3"):
      return render_template("not-right-file.html")
    if file:
      name = request.form['name']
      description = request.form['description']
      filename = secure_filename(random_filename(64) + ".sb3")
      file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/projects/" ,filename))
      new_project = Project(name=name, description=description, project_file=filename, authorid=current_user.id)
      db.session.add(new_project)
      db.session.commit()
      return redirect(url_for('project_page', project_number=new_project.id))
    else:
      return render_template('args-err.html')
  return render_template('create.html')

@app.route('/profile/<int:user_id>/')
def profile_page(user_id):
  user = User.query.filter_by(id=user_id).first()
  if user:
    projects = Project.query.filter_by(authorid=user_id).order_by(Project.id.desc()).all()
    return render_template("profile.html", user=user, projects=projects, textwrap=textwrap)
  else:
    return render_template('profile-404.html', user_id=user_id)

@app.route('/settings/')
@login_required
def settings_page():
  return render_template("settings.html", user=current_user)

@app.route('/settings/', methods=['POST'])
@login_required
def settings_post():
  description = request.form.get('description')
  oldpassword = request.form.get('oldpassword')
  newpassword = request.form.get('newpassword')
  newpasswordconfirm = request.form.get('newpasswordconfirm')
  user = User.query.filter_by(id=current_user.id).first()
  user.description = description
  if newpassword != None and oldpassword != None and newpasswordconfirm != None and newpassword != "" and oldpassword != "" and newpasswordconfirm != "":
    if not check_password_hash(user.password, oldpassword):
      flash("The password you typed isn't correct...")
      return redirect(url_for('settings_page'))      
    if newpassword == newpasswordconfirm:
        user.password = generate_password_hash(newpassword, method='sha256')
    else:
      flash("Your new password and the password confirmation aren't the same...")
      return redirect(url_for('settings_page'))
  db.session.merge(user)
  db.session.commit()
  return redirect(url_for("profile_page", user_id=current_user.id))

@app.route("/signup/")
def signup_page():
  return render_template("signup.html")
@app.route("/login/")
def login_page():
  return render_template("login.html")
@app.route("/credits/")
def credits_page():
  return render_template("credits.html")
@app.route("/project/list/")
def project_list_page():
  projects = Project.query.order_by(Project.id.desc()).all()
  return render_template("project-list.html", projects=projects, textwrap=textwrap)
@app.route('/signup/', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('oh! it seems an user have already this email, sorry :(')
        return redirect(url_for('signup_page'))
    user = User.query.filter_by(name=name).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('oh! it seems an user have already this username, sorry :(')
        return redirect(url_for('signup_page'))
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(realid=random_filename(64), email=email, name=name, password=generate_password_hash(password, method='sha256'), description="Hi! I'm a new user on GroundScratch, but I haven't a description yet... :3", avatar_file=None)

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    # code to validate and add user to database goes here
    return redirect(url_for('login_page'))

@app.route('/login/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash("uh oh... it seems the login details aren't correct...")
        return redirect(url_for('login_page')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('home'))
@app.route("/project_file/<path:path>")
def project_file(path):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + "/projects/", path)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if TESTING==True:
  app.run(host='0.0.0.0', port=PORT)
# TESTING CODE