from flask import Flask, request, render_template, redirect, session, flash
from forms import RegisterForm, LoginForm
from models import db, connect_db, User

app = Flask(__name__)
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
        user = User.register(user.username, user.password)

        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        
        db.session.add(user)
        db.session.commit()
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_user():
    """Produce login form or handle login"""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data
        user = User.authenticate(name, password)

        if user:
            session['username'] = name
            return redirect(f'/users/{name}')
        else:
            form.username.errors = ["Bad name/password"]

    return render_template('login.html', form=form)


@app.route('/secret')
def user_logged_in():
    """Check if user is logged in"""

    if 'username' not in session:
        flash("You must be logged in to view")
        return redirect('/')
    else:
        return render_template('secret.html')


@app.route('/logout')
def logout():
    """Logs out user and redirects to homepage"""

    session.pop('username')
    return redirect('/')

@app.route('/users/<username>')
def display_user_info(username):
    """Displays user info if user is logged in"""

    if 'username' not in session:
        flash("You must be logged in to view")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        return render_template('user.html', user=user)
