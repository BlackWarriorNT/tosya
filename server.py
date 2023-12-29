import json, os, re
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
gui_dir = os.path.join(os.path.dirname(__file__), 'ui')  # development path
if not os.path.exists(gui_dir):  # frozen executable path
    gui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'core')
server = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1  # disable caching
CORS(server)

@server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@server.route('/')
def landing():
    return render_template('ui.html')

@server.route('/base')
def base():
    db = []
    base = open("base.db", "r")
    items = base.readlines()
    for item in items:
        db.append(item.strip())
    return jsonify(db)

@server.route('/send')
def send():
    text = request.args.get('text')
    date = request.args.get('date')
    time = request.args.get('time')
    regul = request.args.get('regul')
    base = open("base.db", "a")
    base.write(str(date)+" "+str(time)+"|"+str(text)+"|"+str(regul)+"\n")
    base.close()
    response = "ok"
    return response

@server.route('/delete')
def delete():
    id = request.args.get('id')
    with open('base.db') as f:
        lines = f.readlines()
    pattern = re.compile(re.escape(id))
    with open('base.db', 'w') as f:
        for line in lines:
            result = pattern.search(line)
            if result is None:
                f.write(line)
    response = "ok"
    return response

def run():
    server.run(host='0.0.0.0', port=5000)