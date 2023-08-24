from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus

app = Flask(__name__)
app.secret_key = "1a2b3c4d5e6d7g8h9i10"

password = "{@dmin2705!}"
encoded_password = quote_plus(password)

username = "VpjAdmin@vpj-staging-postgresql"
encoded_username = quote_plus(username)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"postgresql://{encoded_username}:{encoded_password}@vpj-staging-postgresql.postgres.database.azure.com:5432/your_database?sslmode=require"
print("Connection URL:", app.config["SQLALCHEMY_DATABASE_URI"])

db = SQLAlchemy(app)


# Account model
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)


# Login
@app.route("/pythonlogin/", methods=["GET", "POST"])
def login():
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]

        account = Account.query.filter_by(username=username).first()

        if account and check_password_hash(account.password, password):
            session["loggedin"] = True
            session["id"] = account.id
            session["username"] = account.username
            return redirect(url_for("home"))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template("auth/login.html", title="Login")


# Register
@app.route("/pythonlogin/register", methods=["GET", "POST"])
def register():
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        hashed_password = generate_password_hash(password, method="sha256")

        new_account = Account(username=username, email=email, password=hashed_password)
        db.session.add(new_account)
        db.session.commit()

        flash("You have successfully registered!", "success")
        return redirect(url_for("login"))

    elif request.method == "POST":
        flash("Please fill out the form!", "danger")
    return render_template("auth/register.html", title="Register")


@app.route("/")
def home():
    if "loggedin" in session:
        return render_template(
            "home/home.html", username=session["username"], title="Home"
        )
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if "loggedin" in session:
        return render_template(
            "auth/profile.html", username=session["username"], title="Profile"
        )
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
