from flask import Flask , render_template ,redirect , url_for, request, flash

from Models import db, Todo

app = Flask(__name__)


app.secret_key = "SECRETKEY"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/" , methods =["GET"])
def index():
    todos =Todo.query.all()

    return render_template("index.html", todos = todos)

@app.route("/addtodo", methods = ["POST"])
def add_todo ():
    title = request.form.get("title")
    newTodo = Todo(title = title , complete = False)
    db.session.add(newTodo)
    db.session.commit()

    return redirect(url_for("index"))

@app.route("/state/<int:id>")
def state(id):
    todo = Todo.query.filter_by(id = id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    todo = Todo.query.filter_by(id =id).first()
    db.session.delete(todo)
    db.session.commit()
    flash("Başarıyla silindi","success")

    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
