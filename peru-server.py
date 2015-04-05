#! /usr/bin/env python

import contextlib
import html
import os
import sqlite3

import flask

app = flask.Flask(__name__)

DB_PATH = './peru-server.sqlite3'


@contextlib.contextmanager
def db_connection():
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute('CREATE TABLE blobs (id INTEGER PRIMARY KEY, blob)')
    with sqlite3.connect(DB_PATH) as conn:
        yield conn


def get_blobs():
    with db_connection() as conn:
        rows = conn.execute('SELECT blob FROM blobs ORDER BY id').fetchall()
    blobs = [row[0] for row in rows]
    return ''.join('''
        <p style='white-space: pre-wrap; font-family: monospace'>{}</p>
        <form action="delete/{}" method="POST">
            <input type="submit" value="Delete">
        </form>
    '''.format(html.escape(blob), i) for i, blob in enumerate(blobs))


@app.route('/')
def handle_index():
    return '''
<html>
    <body>
        <form action="submit" method="POST">
            <textarea name="blob" rows="5" cols="80"></textarea><br>
            <input type="submit" value="Submit">
        </form>
{}
    </body>
</html>
'''.format(get_blobs())


@app.route('/submit', methods=['POST'])
def handle_submit():
    blob = flask.request.values['blob']
    with db_connection() as conn:
        conn.execute('INSERT INTO blobs (blob) VALUES (?)', [blob])
    return flask.redirect('/')


@app.route('/delete/<id>', methods=['POST'])
def handle_delete(id=None):
    with db_connection() as conn:
        conn.execute('DELETE FROM blobs WHERE id = ?', [id])
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
