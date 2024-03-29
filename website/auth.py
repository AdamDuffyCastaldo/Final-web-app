from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Users, FaceReference, Note
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import text
from sqlalchemy import select
import base64

auth = Blueprint("auth", __name__)

engine = create_engine("sqlite:///database22.db")

Session = sessionmaker(bind=engine)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        print(firstname)
        lastname = request.form.get("lastname")
        print(lastname)
        print(f"Firstname: {firstname}, Lastname: {lastname}")

        image_data = None
        if "image" in request.files:
            image = request.files["image"]
            if image:
                image_data = image.read()
        #print(image_data)
        session = Session()
        user = session.query(Users).filter_by(firstName=firstname, lastName=lastname).first()
        if user:
            user_id = user.user_id
            print(user_id)
            face_image = session.query(FaceReference).filter_by(user_id=user_id).first()


            
            if face_image:
                user_image_data = face_image.image
                print(user_image_data)
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
        print(user)

        if user:
            flash("User already exists", category="error")
            return redirect(url_for("auth.login"))
       
        if "image" in request.files:
            image = request.files["image"]
            if image:
                image_data = image.read()

        if len(firstName) < 2:
            flash("Firstname must be greater than 1 character", category="error")
        elif len(lastName) < 2:
            flash("Lastname must be greater than 1 character", category="error")
        elif len(password) < 7:
            flash("Password must be at least 7 characters", category="error")
        elif password != Cpassword:
            flash("Passwords don't match", category="error")
        else:
            new_user = Users(firstName = firstName, lastName = lastName, password=generate_password_hash(password, method="pbkdf2:sha256"))

            session.add(new_user)
            session.commit()
            new_face = FaceReference(user_id = new_user.user_id, image = image_data)
            session.add(new_face)
            session.commit()
            flash("Account Created!", category="success")
            return redirect(url_for("blue.home"))
        session.close()

    return render_template("signup.html", user=current_user ,stylesheet = "signuppage.css")