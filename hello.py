#! /usr/bin/env python

import html
import flask

app = flask.Flask(__name__)

blobs = []


def get_blobs():
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
    blobs.append(flask.request.values['blob'])
    return flask.redirect('/')


@app.route('/delete/<id>', methods=['POST'])
def handle_delete(id=None):
    blobs.pop(int(id))
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
