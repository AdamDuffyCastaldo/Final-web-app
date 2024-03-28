from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .models import Base
from flask_login import LoginManager



DB_NAME = "database21.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(engine)
    from .models import Users

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