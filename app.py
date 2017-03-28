import os
import logging
from logging.handlers import RotatingFileHandler
from flask import (Flask, render_template,
                   request, redirect, url_for, send_from_directory)
from werkzeug import secure_filename
import hashlib

UPLOAD_FOLDER = './temp'
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 200 megabytes upload file limit
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def transformDomain(file):
    app.logger.info('Info')
    app.logger.info(file)
    return file


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # if the file exists and is valid
        if file and allowed_file(file.filename):
            # Do whatever operations you want to on the file
            file = transformDomain(file)
            # write it using the hash of its original filename
            # as the new filename
            filename_hash = hashlib.sha224(
                file.filename.encode('utf-8')).hexdigest()
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename_hash))
            # TODO: Do something to the file and generate video
            # For now just returns the same file
            return redirect(url_for('uploaded_file',
                                    filename=filename_hash))
    # If GET request, return simple upload HTML
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <h2>WAVs only, please</h2>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    handler = RotatingFileHandler('log.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
