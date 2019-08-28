from flask import Flask, request, render_template, redirect, session, flash
from forms import RegisterForm, LoginForm, FeedbackForm
from models import db, connect_db, User, Feedback

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
        session['username'] = user.username
        return redirect(f'/users/{user.username}')

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


##################################################################


@app.route('/users/<username>')
def display_user_info(username):
    """Displays user info if user is logged in"""

    if 'username' not in session:
        flash("You must be logged in to view")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        feedback = Feedback.query.filter_by(username=f"{username}").all()
        # BAD
        return render_template('user.html', user=user, feedback=feedback)


@app.route("/users/<username>/feedback/add", methods=["GET"])
def display_add_feedback_form(username):

    form = FeedbackForm()

    if 'username' not in session:
        flash("You must be logged in to view")
        return redirect('/login')
    else:
        return render_template("feedback-form.html", form=form, username=username)


@app.route("/users/<username>/feedback/add", methods=["POST"])
def submit_feedback_form(username):

    form = FeedbackForm()

    if form.validate_on_submit():
        feedback = Feedback()
        feedback.title = form.title.data
        feedback.content = form.content.data
        feedback.username = username

        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{username}')


@app.route('/feedback/<feedback_id>/update')
def display_edit_feedback(feedback_id):

    form = FeedbackForm()

    if 'username' not in session:
        flash("You must be logged in to view")
        return redirect('/login')
    else:
        feedback = Feedback.query.get_or_404(feedback_id)
        return render_template('feedback-edit-form.html', form=form, feedback=feedback)


@app.route('/feedback/<feedback_id>/update', methods=["POST"])
def submit_edit_feedback(feedback_id):

    form = FeedbackForm()
    feedback = Feedback.query.get_or_404(feedback_id)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.add(feedback)
        db.session.commit()

    return redirect(f'/users/{feedback.username}')

@app.route('/feedback/<feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):

    feedback = Feedback.query.get_or_404(feedback_id)

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.username}')


##################################################################


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    """Deletes User and feedback from DB"""

    if 'username' not in session:
        flash("You must be logged in to view")
        return redirect('/login')
    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        return redirect('/')
