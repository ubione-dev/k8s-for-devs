from flask import Flask, render_template, request, make_response, g
import os
import socket
import random
import json
import collections

hostname = socket.gethostname()
votes = collections.defaultdict(int)

app = Flask(__name__)

def getOptions():
    option_a = 'Cats'
    option_b = 'Dogs'
    return option_a, option_b

@app.route("/", methods=['POST','GET'])
def hello():
    vote = None
    option_a, option_b = getOptions()
    if request.method == 'POST':
        vote = request.form['vote']
        vote = option_a if vote == "a" else option_b
        votes[vote] = votes[vote] + 1
    with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as fp:
        namespace = fp.read()

    resp = make_response(render_template(
        'index.html',
        option_a=option_a,
        option_b=option_b,
        hostname=hostname,
        namespace=namespace,
        votes_a=votes[option_a],
        votes_b=votes[option_b],
    ))
    return resp


if __name__ == "__main__":
    extra_files = []
    if "development" == os.getenv("FLASK_ENV"):
        app.jinja_env.auto_reload = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        extra_files=[
            "./static/stylesheets/style.css"
        ]

    app.run(
        host='0.0.0.0',
        port=8080,
        extra_files=extra_files
    )
