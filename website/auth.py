from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Users, FaceReference, Note
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from flask_login import login_user, login_required, logout_user, current_user

import base64

auth = Blueprint("auth", __name__)

engine = create_engine("sqlite:///database21.db")

Session = sessionmaker(bind=engine)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("Lastname")
        session = Session()
        user = session.query(Users).filter_by(firstName=firstname, lastName=lastname).first()
        if user:
            flash("Logged in successfully!", category="success")
            login_user(user, remember=True)
            return redirect(url_for("blue.home"))
        else:
            flash("Invalid credentials", category="error")

    return render_template("login.html", user=current_user ,stylesheet = "loginpage.css")



@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form.get("firstname")
        lastName = request.form.get("lastname")
        password = request.form.get("passkey")
        Cpassword = request.form.get("cPasskey")
        image_data = None
        session = Session()
        user = session.query(Users).filter_by(firstName=firstName, lastName=lastName).first()
        session.close()
       
        if "image" in request.files:
            image = request.files["image"]
            if image:
                image_data = image.read()


        if user:
            flash("User already exists", category="error")


        if len(firstName) < 2:
            flash("Firstname must be greater than 1 character", category="error")
        elif len(lastName) < 2:
            flash("Lastname must be greater than 1 character", category="error")
        elif len(password) < 7:
            flash("Password must be at least 7 characters", category="error")
        elif password != Cpassword:
            flash("Passwords don't match", category="error")
        else:
            session = Session()
            new_user = Users(firstName = firstName, lastName = lastName, password=generate_password_hash(password, method="pbkdf2:sha256"))
            new_face = FaceReference(user_id = new_user.user_id, image = image_data)
            session.add(new_user)
            session.add(new_face)
            session.commit()
            flash("Account Created!", category="success")
            return redirect(url_for("blue.home"))
            session.close()

    return render_template("signup.html", user=current_user ,stylesheet = "signuppage.css")