from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)  # just to refernce the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# triple slash for relative path # quadriple slash for absolute

# need to initialize database
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # first column for ID
    content = db.Column(db.String(200), nullable=False)  # second column
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    # date of creation

    def __repr__(self):  # to return a string everytime w create a new element
        return "<Task %r>" % self.id
    # will return task and the ID of that task


# setting up route
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # for grabbing the content from the form
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        # now putting it into the database with try except block
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")  # redirect back to index page
        except:
            return "There was an issue adding your data"
    else:
        # to look at database contents the way they were created
        tasks = Todo.query.order_by(Todo.date_created).all()
        # passing to the template
        return render_template("index.html", tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "there was a problem deleting that task"


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect("/")
        except:
            return "There was an issue updating your task"
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    # if there is some error then it will pop up on the page
    app.run(debug=False)
