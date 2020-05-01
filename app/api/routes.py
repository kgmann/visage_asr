import os

from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename

from app.api import bp
from app.api.models import STTInputItem, STTOutputItem
from app.api.errors import error_response, bad_request

@bp.route('/tts', methods = ['POST'])
def speech_to_text():
    # check if the post request has the file part
    if 'audio' not in request.files:
        return bad_request('Audio file not present in the request')
    file = request.files.get('audio')

    # if user does not select file, browser also submit an empty part without filename
    if file.filename == '':
        return bad_request('Invalid audio file')
    # check file name and format
    if not STTInputItem.allowed_file(file.filename):
        return bad_request('Invalid audio file name or format')

    # Save file
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename))
        return STTOutputItem.to_dict('File saved')

