from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, Note, Users
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, send_file
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note, Files
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename
import json
import os
import uuid
from flask import current_app, send_from_directory
from io import BytesIO

blue = Blueprint('blue', __name__)

engine = create_engine("sqlite:///ProjectDatabaseFinal.db")
    

Session = sessionmaker(bind=engine)
session = Session()


@blue.route('/', methods=["GET", "POST"])
@login_required
def home():
    user_files = session.query(Files).filter_by(userId=current_user.user_id).all()
    files = [file.FileName for file in user_files]
    # fileContent = [file.FileContent for file in user_files]
    # print(fileContent)
    current_user_images = []
    pdfs = []
    for file in files:
        if os.path.splitext(file)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']:
            if os.path.splitext(file)[1].lower() == ".pdf":
                pdfs.append(file)
            else:
                current_user_images.append(file)
    print(current_user_images)

    user_notes = session.query(Note).filter_by(user_id=current_user.user_id).all()
    if request.method == "GET":
        return render_template("home.html", user=current_user, user_notes=user_notes, image_files = current_user_images, pdf_files = pdfs ,stylesheet = "home.css")

    if request.method == 'POST': 
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(note_text=note, user_id=current_user.user_id)
            session.add(new_note)
            session.commit()
            flash('Note added!', category='success')

    user_notes = session.query(Note).filter_by(user_id=current_user.user_id).all()
    return render_template("home.html", user=current_user, user_notes=user_notes, image_files = current_user_images, pdf_files = pdfs, stylesheet ="home.css")

@blue.route('/deletenote', methods=['POST'])
def deletenote():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = session.query(Note).filter_by(note_id=noteId).first()
    if note:
        if note.user_id == current_user.user_id:
            session.delete(note)
            session.commit()
            return jsonify({})
        
@blue.route('/upload', methods=["POST"])
@login_required
def upload():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part', category='error')
                return redirect(request.url)
            
            file = request.files['file']

            
            if file.filename == '':
                flash('No selected file', category='error')
                return redirect(request.url)
            
            if file:
                filename = file.filename
                unique_identifier = filename
                extension = os.path.splitext(filename)[1].lower()
                if extension not in [".pdf"]:
                    unique_identifier = str(uuid.uuid4())+extension

                if extension not in current_app.config["ALLOWED_EXTENSIONS"]:
                    flash("Unsupported File Type", "error")
                    return redirect(url_for('blue.home'))




                new_file = Files(userId = current_user.user_id, FileContent = file.read() , FileName = unique_identifier, Extension = extension)
                session.add(new_file)
                session.commit()


                #file.save(os.path.join(current_app.config["UPLOAD_DIRECTORY"],unique_identifier))

                flash('File uploaded successfully!', category='success')
                return redirect(url_for('blue.home'))  
    except RequestEntityTooLarge:
        flash("File Exceeds Size Limit", category="error")

    return redirect(url_for('blue.home'))


@blue.route("/produce_file/<path:filename>", methods = ["GET"])
def produce_file(filename):
    print(filename)
    file = session.query(Files).filter_by(FileName = filename).first()
    file_extension = file.Extension
    if file and file_extension in [".png", ".jpg", ".jpeg"]:
        file_content = file.FileContent
        return send_file(BytesIO(file_content), mimetype=f"image/{file_extension[1:]}")
    elif file_extension in [".pdf"]:
        file_content = file.FileContent
        return send_file(BytesIO(file_content), mimetype="application/pdf")
    else:
        return send_from_directory(current_app.config["UPLOAD_DIRECTORY"], filename)
    

@blue.route("/delete_file/<path:filename>", methods = ["POST"])
def delete_file(filename):
    try:
        file = session.query(Files).filter_by(FileName=filename).first()
        if file:
            if file.userId == current_user.user_id:
                session.delete(file)
                session.commit()
                flash('File deleted successfully!', category='success')
            else:
                flash('You are not authorized to delete this file!', category='error')
        else:
            flash('File not found!', category='error')
    except Exception as e:
        flash('An error occurred while deleting the file!', category='error')
        print(f"Error deleting file: {e}")

    return redirect(url_for('blue.home'))