#! /usr/bin/env python

import collections
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
        rows = conn.execute(
            'SELECT id, blob FROM blobs ORDER BY id').fetchall()
    blobs = collections.OrderedDict()
    for id, blob in rows:
        blobs[id] = blob
    return blobs


def get_blob_markup():
    return ''.join('''
        <p style='white-space: pre-wrap; font-family: monospace'>{}</p>
        <form action="delete/{}" method="POST">
            <input type="submit" value="Delete">
        </form>
    '''.format(html.escape(blob), i) for i, blob in get_blobs().items())


@app.route('/')
def handle_index():
    return '''
<html>
    <body>
        <h1>Peru Server</h1>
        <p>To use these module definitions, add <a href='{url}'>{url}</a> to
        your own project file as a <strong>curl</strong> module.</p>
        <h2>Add a new module</h2>
        <form action="submit" method="POST">
            <textarea name="blob" rows="5" cols="80"></textarea><br>
            <input type="submit" value="Submit">
        </form>
        <h2>Existing modules</h2>
{modules}
    </body>
</html>
'''.format(url=flask.url_for('handle_peru_yaml', _external=True),
           modules=get_blob_markup())


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
