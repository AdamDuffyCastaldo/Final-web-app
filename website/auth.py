from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Users, FaceReference, Note
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import numpy as np
from flask_login import login_user, login_required, logout_user, current_user
import base64
import io
from flask import make_response
import os
import sys


path_to_encode_face = os.path.join(os.getcwd(), "facialscripts")
sys.path.append(path_to_encode_face)

from facialscripts import encode_face

auth = Blueprint("auth", __name__)

engine = create_engine("sqlite:///ProjectDatabaseFinal.db")

Session = sessionmaker(bind=engine)

def blob_to_nparray(blob_data):
    try:

        image = Image.open(io.BytesIO(blob_data))
        
        image_np = np.array(image)
        
        return image_np
    except Exception as e:
        print("Error:", e)
        return None

def converttorgb(png_array):
    rgb_array = png_array[:, :, :3]
    image = Image.fromarray(rgb_array.astype("uint8"))
    return image

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", user=current_user, stylesheet="loginpage.css")
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        image = request.files.get("image")
        print(firstname, lastname, password)
        errors = []
        if not firstname:
            errors.append("Firstname is required")
        if not lastname:
            errors.append("Lastname is required")
        if not password:
            errors.append("Password is required")
        if image.filename == "empty.png":
            errors.append("Image is required")
        if errors:
            for error in errors:
                flash(error, category="error")
            error_message = ", ".join(errors)
            print(error_message)
            return jsonify({"error": True, "message": error_message})

        image_data = None
        if "image" in request.files:
            image = request.files["image"]
            if image:
                image_data = image.read()
        #print(image_data)
        session = Session()
        try:
            user = session.query(Users).filter_by(firstName=firstname, lastName=lastname).first()
            if user:
                user_id = user.user_id
                face_image = session.query(FaceReference).filter_by(user_id=user_id).first()
                print(f"Firstname: {firstname}, Lastname: {lastname}")
                if face_image:
                    database_image = face_image.image
                    database_image = blob_to_nparray(database_image)
                    database_image = converttorgb(database_image)
                    database_image.save("databaseimage.jpg")

                    image_data = blob_to_nparray(image_data)
                    image_data = converttorgb(image_data)
                    image_data.save("inputimage.jpg")

                    Faces_same = encode_face.compareImages("databaseimage.jpg", "inputimage.jpg")
                    if Faces_same.item() == 1:
                        issamepredict = True
                    else:
                        issamepredict = False

                    print(issamepredict)

                    if issamepredict and password and check_password_hash(user.password, password):
                        login_user(user, remember=True)
                        flash("Logged in successfully!", category="success")
                        return jsonify({"issamepredict": issamepredict})
                    else:
                        flash("Face not recognized", category="error")
                else:
                    flash("User not found. Please check credentials", category="error")
  
            else:
                flash("User not found. Please check credentials", category="error")

        finally:
            session.close()
    
    return jsonify({"issamepredict": False})



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
        image = request.files.get("image")
        print(firstName, lastName, password, Cpassword)

        if len(firstName) < 2:
            flash("Firstname must be greater than 1 character", category="error")
            return jsonify({"isAccountCreated": False, "errorMessage": "Firstname must be greater than 1 character"})
        elif len(lastName) < 2:
            flash("Lastname must be greater than 1 character", category="error")
            return jsonify({"isAccountCreated": False, "errorMessage": "Lastname must be greater than 1 character"})
        elif len(password) < 7:
            flash("Password must be at least 7 characters", category="error")
            return jsonify({"isAccountCreated": False, "errorMessage": "Password must be at least 7 characters"})
        elif password != Cpassword:
            flash("Passwords don't match", category="error")
            return jsonify({"isAccountCreated": False, "errorMessage": "Passwords don't match"})
        
        if not image or image.filename == 'empty.png':
            flash("Image is required", category="error")
            return jsonify({"isAccountCreated": False, "errorMessage": "Image is required"})
        
        image_data = image.read()
        session = Session()
        try:
            existing_user = session.query(Users).filter_by(firstName=firstName, lastName=lastName).first()
            if existing_user:
                flash("User already exists with the same first name and last name", category="error")
                return jsonify({"isAccountCreated": False, "errorMessage": "User already exists with the same first name and last name"})

            new_user = Users(firstName=firstName, lastName=lastName, password=generate_password_hash(password, method="pbkdf2:sha256"))
            session.add(new_user)
            session.commit()

            new_face = FaceReference(user_id=new_user.user_id, image=image_data)
            session.add(new_face)
            session.commit()

            login_user(new_user, remember=True)
            flash("Account Created!", category="success")
            return jsonify({"isAccountCreated": True})

        finally:
            session.close()

    return render_template("signup.html", user=current_user, stylesheet="signuppage.css")

