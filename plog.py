from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#create a Flask instance
app = Flask(__name__)
#add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'

#key
app.config['SECRET_KEY'] = "secret key 1 2 3"

#initialize database
db = SQLAlchemy(app)

#create Model
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    rec = db.Column(db.String(200), nullable=False, unique=True)
    dateAdded = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r' % self.name

with app.app_context():
    db.create_all()
    

#create a From class
class MovieForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    rec = StringField("Movie Rec", validators=[DataRequired()])
    submit = SubmitField("Submit")


#create a From class
class NamerForm(FlaskForm):
    name = StringField("Whats Your Name", validators=[DataRequired()])
    submit = SubmitField("Submit")



#create a route decorator
@app.route('/')

# FILTERS
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags
#etc...


def index():
    first_name = "Nicholas"
    elements = ["About Me", "Projects", "Relevant Coursework", "Secondary Hobbies"]
    return render_template("index.html", 
        first_name = first_name,
        elements = elements)


#localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    languages = ['Python', 'C++', 'HTML', 'CSS', 'JS']
    libraries = ['Sqlite3', 'Tkinter', 'Flask', 'Jinja2', 'Bootstrap']
    fields = ['Database Systems', 'Software Engineering', 'Software developer', 'Web developer', 'Algorithms']
    return render_template("user.html", 
        user_name=name,
        languages = languages,
        libraries = libraries,
        fields = fields)

@app.route('/workoutdatabase')
def Databaseproject():
    return render_template("workoutdatabase.html")

@app.route('/rle-encoder')
def rle_encoder():
    return render_template("rle_encoder.html")

@app.route('/rle-encoder/multi-threaded')
def rle_multithreaded():
    return render_template("rle_multithreaded.html")

@app.route('/rle-encoder/clientserver')
def rle_client_server():
    return render_template("rle_clientserver.html")

@app.route('/lettergradecalculator')
def letterGradeCalc():
    return render_template("letterGradeCalculator.html")

@app.route('/relevantcoursework')
def relevantCourseWork():
    courseWork =["Algorithms and Data structures ", "Operating Systems", "Automata and Computability", "Computer organization and Architechture", "Linear Algebra", "Discrete Math", "Statistics", "Software Design"]
    return render_template("relevantwork.html",
        courseWork = courseWork)

@app.route('/watch-collecting')
def watchCollecting():
    return render_template("watchcollection.html")

@app.route('/lifting-weights')
def liftingWeights():
    return render_template("bodybuilding.html")

@app.route('/movies', methods=['GET', 'POST'])
def movies():
    name = None
    form = MovieForm()
    if form.validate_on_submit():
        mov= Movies.query.filter_by(rec = form.rec.data).first()
        if mov is None:
            mov = Movies(name = form.name.data, rec = form.rec.data)
            db.session.add(mov)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.rec.data = ''
        flash("Movie Recommendation added Successfully")
    our_movies = Movies.query.order_by(Movies.dateAdded)
    return render_template("movies.html", 
        form = form,
        name = name,
        our_movies=our_movies)






# create custom error pages

# invalid url
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# internal server error
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# create name page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    #validate form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successfully!")

    return render_template("name.html",
        name = name,
        form = form)