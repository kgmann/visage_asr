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
    def is_valid(data):
        if 'audio' not in data:
            return False
        return True
    
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
