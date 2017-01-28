from flask import Flask
import re
import os
app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Watch out for your nuke codes :^)"

@app.route('/file/<folder>')
def display_cont(folder):
    if re.search('(\\|\.)', folder):
        return "Hey now"
    files = os.listdir("data/" + folder)
    ret = ""
    for name in files:
        ret = ret + name + "\n"
        print name
    return ret

@app.route('/file/<folder>/<filename>')
def get_file(folder, filename):
    if re.search('(\\|\.)', folder) or re.search('(\\|\.)', filename):
        return "Stop that."
    raw = open('data/' + folder + "/" + filename, "r")
    return raw.read()


if __name__ == '__main__':
    app.run(host='0.0.0.0')
