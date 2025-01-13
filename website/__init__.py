from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .models import Base
from flask_login import LoginManager
import os


DB_NAME = "ProjectDatabaseFinal.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config["MAX_CONTENT_LENGTH"] = 16*1024*1024
    app.config["ALLOWED_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".gif", ".pdf"]
    app.config["UPLOAD_DIRECTORY"] = os.path.join(os.path.dirname(__file__), '..', 'uploads')


    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(engine)
    from .models import Users, Note, FaceReference

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    Session = sessionmaker(bind=engine)
    @login_manager.user_loader
    def load_user(id):
        session = Session()
        return session.query(Users).get(int(id))
    

    from .blue import blue
    from .auth import auth
    app.register_blueprint(blue, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app