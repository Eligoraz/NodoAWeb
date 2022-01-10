from enum import unique
from os import name
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import validators
from wtforms.form import Form
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a Flask Instance
app = Flask(__name__)
# Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# Secrete Key
app.config['SECRET_KEY'] = "clave super secreta"
# Initialize The Database
db = SQLAlchemy(app)
# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create A String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create a User Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Form Class
class NamerForm(FlaskForm):
    name = StringField("Cual es tu nombre", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("User Added Successfully!")
    our_user = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", 
        form=form,
        name=name,
        our_users=our_user)

# Create a route decorator
@app.route('/')

def index():
    first_name = "Raul"
    stuff = "this is bold text"

    favorite_pizza = ["Pepperoni", "Cheese", "Aceitunas"]
    return render_template("index.html",
        first_name=first_name,
        stuff=stuff,
        favorite_pizza=favorite_pizza)

#localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    #retorna el valor escrito en el buscador como una pagina
    #return "<h1>Hola {}</h1>".format(name)
    return render_template("user.html", user_name=name)

#Create Custom Error Pages
#Invalid URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"), 500

#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
    name = None
    form = NamerForm()
    # Validate Form
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Form Submitted Successful")
    return render_template("name.html",
        name = name,
        form = form)
#Con este codigo puedo llamar el archivo desde consola y corre el servidor
if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT, 8080")))