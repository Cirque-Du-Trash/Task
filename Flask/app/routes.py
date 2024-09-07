from flask import (jsonify, render_template, request, Blueprint, redirect, url_for, flash, session)
from werkzeug.security import check_password_hash
from .models import Question, Participant, Quiz, Admin
from .database import db
from sqlalchemy import func
from plotly.offline import plot
from datetime import datetime
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import plotly
import json

main = Blueprint("main", __name__)
admin = Blueprint("admin", __name__, url_prefix="/admin/")


@main.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@main.route("/participants", methods=["POST"])
def add_participant():
    data = request.get_json()
    new_participant = Participant(
        name=data["name"], age=data["age"], gender=data["gender"], created_at=datetime.utcnow()
    )
    db.session.add(new_participant)
    db.session.commit()
    return jsonify({"redirect": url_for("main.quiz"), "participant_id": new_participant.id})


@main.route("/quiz")
def quiz():
    participant_id = request.cookies.get("participant_id")
    if not participant_id:
        return redirect(url_for("main.home"))

    questions = Question.query.all()
    return render_template("quiz.html", questions=[q.content for q in questions])


@main.route("/submit", methods=["POST"])
def submit():
    participant_id = request.cookies.get("participant_id")
    if not participant_id:
        return jsonify({"error": "Participant ID not found"}), 400

    quizzes = request.json.get("quizzes", [])
    for quiz in quizzes:
        db.session.add(Quiz(participant_id=participant_id, question_id=quiz["question_id"], chosen_answer=quiz["chosen_answer"]))
    
    db.session.commit()
    return jsonify({"message": "Quiz answers submitted successfully.", "redirect": url_for("main.show_results")})


@main.route("/questions")
def get_questions():
    questions = Question.query.filter_by(is_active=True).order_by(Question.order_num).all()
    return jsonify(questions=[{"id": q.id, "content": q.content, "order_num": q.order_num} for q in questions])


@main.route("/results")
def show_results():
    participants_df = pd.DataFrame([{"age": p.age, "gender": p.gender} for p in Participant.query.all()])
    quizzes_df = pd.DataFrame([{"question_id": q.question_id, "chosen_answer": q.chosen_answer, "participant_age": q.participant.age} for q in Quiz.query.join(Question).all()])

    fig_age = create_pie_chart(participants_df, "age", "Age Distribution")
    fig_gender = create_pie_chart(participants_df, "gender", "Gender Distribution")

    quiz_response_figs = create_quiz_response_figs(quizzes_df)
    
    graphs_json = json.dumps({
        "age_distribution": fig_age,
        "gender_distribution": fig_gender,
        "quiz_responses": quiz_response_figs,
    }, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("results.html", graphs_json=graphs_json)


def create_pie_chart(df, column, title):
    fig = px.pie(df, names=column, hole=0.3, title=title)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def create_quiz_response_figs(quizzes_df):
    quiz_response_figs = {}
    for question_id in quizzes_df["question_id"].unique():
        filtered_df = quizzes_df[quizzes_df["question_id"] == question_id]
        fig = px.histogram(
            filtered_df,
            x="chosen_answer",
            title=f"Question {question_id} Responses",
            color="chosen_answer",
            barmode="group",
            category_orders={"chosen_answer": ["yes", "no"]},
            color_discrete_map={"yes": "RebeccaPurple", "no": "LightSeaGreen"},
        )
        style_histogram(fig)
        quiz_response_figs[f"question_{question_id}"] = fig
    return quiz_response_figs


def style_histogram(fig):
    fig.update_layout(
        xaxis_title="Chosen Answer",
        yaxis_title="Count",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
        title_font=dict(family="Helvetica, Arial, sans-serif", size=22, color="RebeccaPurple"),
    )
    fig.update_traces(marker_line_width=1.5, opacity=0.6)


@admin.route("", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password, password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid username or password")

    return render_template("admin.html")


@admin.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("admin.login"))


from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_logged_in" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorated_function


@admin.route("dashboard")
@login_required
def dashboard():
    participant_counts = db.session.query(
        func.date(Participant.created_at).label("date"),
        func.count(Participant.id).label("count"),
    ).group_by("date").all()

    dates = [result.date for result in participant_counts]
    counts = [result.count for result in participant_counts]

    graph = go.Figure(go.Scatter(x=dates, y=counts, mode="lines+markers"))
    graph.update_layout(title="일자별 참가자 수", xaxis_title="날짜", yaxis_title="참가자 수")
    graph_div = plot(graph, output_type="div", include_plotlyjs=False, config={'displayModeBar': False})

    return render_template("dashboard.html", graph_div=graph_div)


@admin.route("/dashboard/question", methods=["GET", "POST"])
@login_required
def manage_questions():
    if request.method == "POST":
        handle_question_form(request.form)

    questions = Question.query.order_by(Question.order_num).all()
    return render_template("manage_questions.html", questions=questions)


def handle_question_form(form):
    if "new_question" in form:
        is_active = "is_active" in form and form["is_active"] == "on"
        new_question = Question(content=form["content"], order_num=form["order_num"], is_active=is_active)
        db.session.add(new_question)
    else:
        question = Question.query.get(form["question_id"])
        if question:
            question.content = form["content"]
            question.order_num = form["order_num"]
            question.is_active = "is_active" in form and form["is_active"] == "on"
    db.session.commit()


@admin.route("/dashboard/list")
@login_required
def quiz_list():
    quizzes = Quiz.query.all()
    return render_template("quiz_list.html", quizzes=quizzes)