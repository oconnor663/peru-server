#! /usr/bin/env python

import html
import flask

app = flask.Flask(__name__)

blobs = []


@app.route('/')
def hello_world():
    return '''
<html>
    <body>
        <form action="submit" method="POST">
            <textarea name="blob"></textarea><br>
            <input type="submit" value="Submit">
        </form>
            <div style='white-space: pre-wrap; font-family: monospace'>
{}
            </div>
    </body>
</html>
'''.format(get_blobs())


def get_blobs():
    return "".join(
        "<p>" + html.escape(blob) + "</p>\n"
        for blob in blobs
    )


@app.route('/submit', methods=['POST'])
def submit():
    blobs.append(flask.request.values['blob'])
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
