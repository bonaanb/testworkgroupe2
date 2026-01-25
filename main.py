from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from data import (
    init_db, show_tasks, insert_task, delete_task,
    add_completed, show_completed, get_task_by_id,
    create_user, get_user
)

app = Flask(__name__)
app.secret_key = "secret-key"

init_db()


# ---------- AUTH ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        password_hash = generate_password_hash(password)

        try:
            create_user(username, password_hash)
            flash("Регистрация прошла успешно ✅")
            return redirect(url_for("login"))
        except:
            flash("Пользователь уже существует ❌")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = get_user(username)

        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            return redirect(url_for("index"))

        flash("Неверный логин или пароль ❌")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------- MAIN ----------
@app.route("/", methods=["GET", "POST"])
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            insert_task(task, user_id)
        return redirect(url_for("index"))

    tasks = show_tasks(user_id)
    return render_template("index.html", tasks=tasks)


@app.route("/complete/<int:task_id>")
def complete(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    task = get_task_by_id(task_id, user_id)

    if task:
        add_completed(task[0], user_id)
        delete_task(task_id, user_id)

    return redirect(url_for("index"))


@app.route("/completed")
def completed_page():
    if "user_id" not in session:
        return redirect(url_for("login"))

    completed = show_completed(session["user_id"])
    return render_template("completed.html", completed=completed)


@app.route("/delete/<int:task_id>")
def delete(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_task(task_id, session["user_id"])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
