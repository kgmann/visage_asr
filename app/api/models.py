from app.api.errors import error_response, bad_request
from app.api.utils import convert_and_save

class STTInputItem(object):
    """
    This class is intended to Get Api data input and
    make all required validations and other related
    operations.
    """
    def __init__(self, audio, config=None):
        self.audio = audio
        self.config = config
    
    @staticmethod
    def from_dict(data):
        api_input = {}
        api_input['audio'] = data['audio']
        api_input['config'] = data['config']

        return api_input

    @staticmethod
    def to_dict(audio, config=None):
        api_input = {}
        api_input['audio'] = audio
        api_input['config'] = config

        return api_input

    @staticmethod
    def check_errors(data):
        """
        Validate request data. (neglect config param for the moment)
        :return: Error Message on error and None if OK
        """
        if 'audio' not in data:
            return bad_request("Invalid request: Missing audio field.")
        if not ('uri' in data['audio'] or 'content' in data['audio']):
            return bad_request("Invalid request: Neither 'uri' nor 'content' not found in request. Use one of them.")
        if 'uri' in data['audio'] and 'content' in data['audio']:
            return bad_request("Invalid request: Use either 'uri' or 'content' in request.")
        if data['audio'].get('uri') is None and data['audio'].get('content') is None:
            return bad_request("Invalid request: Audio file not present in the request.")

        if 'uri' in data['audio']:
            return error_response(501, "Operation not Implemented: audio file through 'uri' is not yet supported. Use 'content' instead")

        return None

    @staticmethod
    def get_audio(data):
        """
        Return the audio data from 'uri' or 'content' field
        """
        if 'audio' not in data:
            return None
        if not ('uri' in data.get('audio') or 'content' in data.get('audio')):
            return None
        
        if 'content' in data.get('audio'):
            audio = convert_and_save(data.get('audio').get('content'))
        
        return audio

    
    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'wav', 'mp3'}
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class STTOutputItem(object):
    """
    This class is intended to Get Api data input and
    make all required validations and other related
    operations.
    """
    def __init__(self, result, error=None):
        self.error = error
        self.data = {'RecognitionResult', result}
    
    @staticmethod
    def from_dict(data):
        api_input = {}
        api_input['audio'] = data['audio']
        api_input['config'] = data['config']

        return api_input

    @staticmethod    
    def to_dict(result, config=None):
        api_input = {}
        api_input['RecognitionResult'] = result

        return {"result" : api_input}
