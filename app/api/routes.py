import os

from flask import request, jsonify, current_app
from werkzeug.utils import secure_filename

from app.api import bp
from app.api.models import STTInputItem, STTOutputItem
from app.api.errors import error_response, bad_request

@bp.route('/tts', methods = ['POST'])
def speech_to_text():
    """
    Get API request, parse json, process and return response.
    :return: json
    """

    request_data = request.get_json() or {}

    errors = STTInputItem.check_errors(request_data)

    # Return errors if the request is invalid
    if errors is not None:
        return errors

    filepath = STTInputItem.get_audio(request_data)
    if filepath is None:
        bad_request('Something is wrong with the audio file')

    filename = os.path.basename(filepath)

    # Return response
    return STTOutputItem.to_dict('File saved')

