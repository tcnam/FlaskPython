from flask import Flask, redirect, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class ToDo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed=db.Column(db.Integer, default=0)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r %s>' % (self.id, self.content)


@app.route('/',methods=['POST', 'GET'])
def index():
    if request.method=='POST':
        task_content=request.form['content']
        if task_content!="":
            new_task=ToDo(content=task_content)
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an issue adding your task"
        else:
            return redirect('/')
    else:
        tasks= ToDo.query.order_by(ToDo.date_created).all()
        print(tasks)
        return render_template("index.html",tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task"

    

if __name__=="__main__":
    app.run(debug=True)