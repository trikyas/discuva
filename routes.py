from flask import Flask, render_template
from app.models import db
from forms import signupForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'pastgressql://localhost/discuva'
db.init_app(app)
app.secret_key = "development-key"

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/signup")
def signup():
    form = signupForm()
    return render_template("signup.html", form=form)
    
if __name__ == "__main__":
    app.run(debug=True)