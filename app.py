from flask import (
    Flask,
    render_template,
    send_from_directory
)
from flask_moment import Moment
from datetime import datetime
import os

def byte_units(value, units=-1):
    UNITS=('Bytes', 'KB', 'MB', 'GB', 'TB', 'EB', 'ZB', 'YB')
    i=1
    value /= 1000.0
    while value > 1000 and (units == -1 or i < units) and i+1 < len(UNITS):
        value /= 1000.0
        i += 1
    return f'{round(value,3):.3f} {UNITS[i]}'


app = Flask(__name__)
# Get current path
path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.jinja_env.filters.update(byte_units = byte_units)
moment = Moment(app)

try:
    os.makedirs(app.config['UPLOAD_FOLDER'])
except:
    pass

def get_files(target):
    for file in os.listdir(target):
        path = os.path.join(target, file)
        if os.path.isfile(path):
            yield (
                file,
                datetime.utcfromtimestamp(os.path.getmtime(path)),
                os.path.getsize(path)
            )

@app.route('/')
def index():
    files = get_files(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', **locals(), variable = UPLOAD_FOLDER)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=False,threaded=True)