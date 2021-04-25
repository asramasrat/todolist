from flask import Flask, render_template, json, request, session, redirect, url_for
from config import Config
from peewee import *

app = Flask(__name__)
app.config.from_object(Config)
# db = SqliteDatabase('tasks.db',timeout=3, pragmas={'journal_mode': 'wal'})
mysql_db = MySQLDatabase('sql6406870', user='sql6406870', password='Qvr3TpU6Kx',
                         host='sql6.freemysqlhosting.net', port=3306)


class Task(Model):
	id = IntegerField(primary_key=True)
	name = CharField()
	is_completed = BooleanField(default=False)
	class Meta:
		database = mysql_db


@app.route('/')
def index():
	return render_template("index.html", tasks=Task.select())

@app.route('/add',methods=['GET', 'POST'])
def add():
	_name = request.form['name']
	task = Task(name=_name, is_completed=False)
	task.save()
	return redirect('/')


@app.route('/changecomp/<id>')
def change(id):
	task = Task.get(Task.id == id)
	if task.is_completed == True:
		task.is_completed = False
	else:
		task.is_completed=True
	task.save()
	return redirect('/', code=302)

@app.route('/delete/<id>')
def delete(id):
	task = Task.get(Task.id == id)
	task.delete_instance()
	return redirect('/', code = 302)


if __name__ == '__main__':
    app.run(threaded=True, port=5000)