from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from .models import Base, Note, Users
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
import json


blue = Blueprint('blue', __name__)
    
    # Create an engine instance for database operations
engine = create_engine("sqlite:///database21.db")
    
Session = sessionmaker(bind=engine)
session = Session()
    
@blue.route('/', methods=["GET", "POST"])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')  # Gets the note from the HTML
    
        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(note_text=note, user_id=current_user.user_id)  # Providing the schema for the note
            session.add(new_note)  # Adding the note to the database
            session.commit()
            flash('Note added!', category='success')
    
    return render_template("home.html", user=current_user)

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