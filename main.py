import random
import sqlite3

from flask import (
    Flask,
    render_template,
    g,
    redirect,
    request,
)

app = Flask(__name__)


########## LABELS ##########

labels = ['神経質', '短気', '無気力', '負けず嫌い', '寛容']
num_labels = len(labels)


########## DB ##########

DATABASE = 'sqlite3.db'

def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


########## DATASET ##########

def get_count_column():
    return query_db(
            'SELECT COUNT(id) FROM dataset', one=True)[0]

def exists(identifier):
    _identifier = query_db(
            'SELECT id FROM dataset WHERE id = ?',
            (identifier,), True)[0]
    return False if _identifier is None else True

def update_label(identifier, label):
    db = get_db()
    db.execute(
        'UPDATE dataset SET {} = {} + 1 WHERE id = ?'.format(label, label),
        (identifier,))
    db.commit()


########## APP ##########

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/vote', methods=('GET', 'POST'))
def vote():
    if request.method == 'POST':
        identifier = int(request.form['id'])
        label = int(request.form['label'])
        value = 'y' if request.form['value'] == 'はい' else 'n'

        if exists(identifier):
            label = 'label{}{}'.format(label, value)
            update_label(identifier, label)

        return redirect('/vote')

    if request.method == 'GET':
        count = get_count_column()

        if count == 0:
            redirect('/')

        identifier = random.randint(1, count)
        filepath = query_db(
            'SELECT filepath FROM dataset WHERE id = ?',
            (identifier,), True)[0]
        label_index = random.randint(0, num_labels-1)

        return render_template('vote.html', id=identifier,
                    filepath=filepath, label=label_index, type=labels[label_index])


if __name__ == "__main__":
    app.run(debug=True)
