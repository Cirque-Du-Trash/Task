from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
import os
import click
from .models import Question, Admin, Participant
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "oz_coding_secret"

    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    dbfile = os.path.join(basedir, "db.sqlite")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + dbfile
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    from routes import main as main_blueprint
    from routes import admin as admin_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)

    def add_initial_questions():
        initial_questions = [
            "오즈코딩스쿨에 대해서 알고 계신가요?",
            "프론트엔드 과정에 참여하고 계신가요?",
            "전공자 이신가요?",
            "프로젝트를 진행해보신적 있으신가요?",
            "개발자로 일한 경력이 있으신가요?",
        ]
        yesterday = datetime.utcnow() - timedelta(days=1)

        if not Admin.query.filter_by(username="admin").first():
            hashed_password = generate_password_hash("0000")
            db.session.add(Admin(username="admin", password=hashed_password))

        participants_without_created_at = Participant.query.filter(Participant.created_at == None).all()

        for participant in participants_without_created_at:
            participant.created_at = yesterday

        for question_content in initial_questions:
            if not Question.query.filter_by(content=question_content).first():
                db.session.add(Question(content=question_content))

        for question in Question.query.all():
            question.order_num = question.id
            question.is_active = True
        
        db.session.commit()

    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        db.create_all()
        add_initial_questions()
        click.echo("Initialized the database.")

    app.cli.add_command(init_db_command)

    return app
