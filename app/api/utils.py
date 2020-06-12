import os
import time
import base64

from flask import current_app
from werkzeug.utils import secure_filename

def convert_and_save(b64_string, extension="wav", filename=None):
    """
    Convert file from base64 to audio and save
    """
    if filename is None:
        filename = "".join(str(time.time()).split('.')) + "." + extension
    
    filepath = os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename)    
    with open(filepath, "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))
    
    return filepath

def save_audio(request_file, filename=None):
    """
    Get audio from request and save it to a file
    """
    if filename is None:
        filename = secure_filename("".join(str(time.time()).split('.')) + ".wav")
    filepath = os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename)
    request_file.save(filepath)

    return filepath

def allowed_audio_file(filename):
    ALLOWED_EXTENSIONS = {'wav'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def remove_output_file(output_file_path):
    if os.path.isfile(output_file_path):
        os.remove(output_file_path)
