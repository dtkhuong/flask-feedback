from flask import Flask, request, render_template, redirect
from forms import RegisterForm
from models import db, connect_db, User

app=Flask(__name__)
app.config["SECRET_KEY"] = "VERYSECRET"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLACHEMY_ECHO'] = True

connect_db(app)

@app.route("/")
def redirect_to_register():
    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def show_register_form():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.password = form.password.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        db.session.add(user)
        db.session.commit()
        return redirect("/secret")
    
    else:
        return render_template("register.html", form=form)

