from flask import Blueprint, redirect, render_template, request, url_for

from .extensions import db
from .models import Todo

bp = Blueprint("todos", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()

        if title:
            todo = Todo(title=title)
            db.session.add(todo)
            db.session.commit()

        return redirect(url_for("todos.index"))
    todos = Todo.query.order_by(Todo.created_at.desc()).all()
    return render_template("index.html", todos=todos)

@bp.route("/todos/<int:todo_id>/complete", methods=["POST"])
def complete(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    todo.completed = True
    db.session.commit()

    return redirect(url_for("todos.index"))

@bp.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete(todo_id):
    todo = Todo.query.get_or_404(todo_id)

    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for("todos.index"))