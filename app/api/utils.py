import os
import time
import base64

from flask import current_app

def convert_and_save(b64_string, filename=None):
    """
    Convert file from base64 to audio and save
    """
    if filename is None:
        filename = "".join(str(time.time()).split('.')) + ".wav"
    
    filepath = os.path.join(current_app.config.get('UPLOAD_FOLDER'), filename)
    
    with open(filepath, "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))
    
    return filepath
