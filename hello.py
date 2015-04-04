#! /usr/bin/env python

import flask

app = flask.Flask(__name__)

blobs = []


@app.route('/')
def hello_world():
    return '''
<html>
    <body>
        <form action="submit" enctype="multipart/form-data" method="POST">
            A: <input type="text" name="A"><br>
            B: <input type="text" name="B"><br>
            <input type="submit" value="Submit">
        </form>
        {}
    </body>
</html>
'''.format(get_blobs())


def get_blobs():
    elements = ""
    for blob in blobs:
        elements += "<ul>"
        for key, val in blob.items():
            # XXX: XSS
            elements += "<li>{}: {}</li>".format(key, val)
        elements += "</ul>"
    return elements


@app.route('/submit', methods=['POST'])
def submit():
    print("RECEIVED")
    for key, val in flask.request.values.items():
        print("  {}: {}", key, val)
    blobs.append(flask.request.values)
    return flask.redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
