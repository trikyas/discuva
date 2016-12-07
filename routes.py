from flask import Flask, render_template, request, session, redirect, url_for
from models import db, User
from form import SignupForm, LoginForm, AddressForm

#–––– It must be in the "from" –– "imports".. I can't think of anything else... Please check

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = postgres://atcyhqeissgkmo:2BnJWWm_4SJsVK8gYCFvBJ3cLx@ec2-54-235-123-159.compute-1.amazonaws.com:5432/ddm8qo4clh00q7
db.init_app(app)

app.secret_key = "development-key"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
  if 'email' in session:
    return redirect(url_for('home'))

  form = SignupForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:
      newuser = User(form.first_name.data, form.last_name.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email
      return redirect(url_for('home'))

  elif request.method == "GET":
    return render_template('signup.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
  if 'email' in session:
    return redirect(url_for('home'))

  form = LoginForm()

  if request.method == "POST":
    if form.validate() == False:
      return render_template("login.html", form=form)
    else:
      email = form.email.data 
      password = form.password.data 

      user = User.query.filter_by(email=email).first()
      if user is not None and user.check_password(password):
        session['email'] = form.email.data 
        return redirect(url_for('home'))
      else:
        return redirect(url_for('login'))

  elif request.method == 'GET':
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
  session.pop('email', None)
  return redirect(url_for('index'))

@app.route("/home", methods=["GET", "POST"])
def home():
  if 'email' not in session:
    return redirect(url_for('login'))

  form = AddressForm()

  places = []
  # my place ––– works
  my_coordinates = (-31.9110, 152.4539)

  if request.method == 'POST':
    if form.validate() == False:
      return render_template('home.html', form=form)
    else:
      # get the address ––– works
      address = form.address.data 

      # query for places around it ––– works
      p = Place()
      my_coordinates = p.address_to_latlng(address)
      places = p.query(address)

      # return those results  ––– It is not returning
      return render_template('home.html', form=form, my_coordinates=my_coordinates, places=places)

  elif request.method == 'GET':
    return render_template("home.html", form=form, my_coordinates=my_coordinates, places=places)

if __name__ == "__main__":
    app.debug = True
    app.run()