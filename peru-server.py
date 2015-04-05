#! /usr/bin/env python

import collections
import contextlib
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
        rows = conn.execute(
            'SELECT id, blob FROM blobs ORDER BY id').fetchall()
    blobs = collections.OrderedDict()
    for id, blob in rows:
        blobs[id] = blob
    return blobs


@app.route('/')
def handle_index():
    blobs = get_blobs()
    url = flask.url_for('handle_peru_yaml', _external=True)
    return flask.render_template('index.html', blobs=blobs, url=url)


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


@app.route('/peru.yaml')
def handle_peru_yaml():
    return flask.Response(
        '\n'.join(get_blobs().values()),
        mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
