from flask import Flask, render_template, request, redirect, url_for
from data import show_tasks, insert_task, delete_task, init_db, add_completed, show_completed, get_task_by_id


app = Flask(__name__)

init_db()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")

        if task:
            insert_task(task)
        return redirect(url_for("index"))

    tasks = show_tasks()

    return render_template("index.html", tasks=tasks)

@app.route("/complete/<int:task_id>")
def complete(task_id):
    task = get_task_by_id(task_id)
    if task:
        add_completed(task[0])
        delete_task(task_id)
    return redirect(url_for("index"))

@app.route("/completed")
def completed_page():
    completed = show_completed()
    return render_template("completed.html", completed=completed)

if __name__ == '__main__':
    app.run()
