import os
import tempfile

import sox


from app.api.errors import error_response, bad_request
from app.api.utils import convert_and_save

class STTInputItem(object):
    """
    This class is intended to Get Api data input and
    make all required validations and other related
    operations.
    """
    
    ALLOWED_EXTENSIONS = {'wav', 'ogg', 'mp3', 'gsm'}

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
        if 'config' not in data:
            return bad_request("Invalid request: Missing 'config' field in the request parameters.")
        if 'format' not in data['config']:
            return bad_request("Invalid request: Missing 'format' in 'config' field in the request parameters.")
        if data['config']['format'] not in STTInputItem.ALLOWED_EXTENSIONS:
            return bad_request("Invalid input file format: The 'format' specified is either invalid or not supported by the API.")

        if 'audio' not in data:
            return bad_request("Invalid request: Missing audio field in the request parameters.")
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
        if ('config' not in data) or ('format' not in data['config']):
            return None
        if 'audio' not in data:
            return None
        if not ('uri' in data.get('audio') or 'content' in data.get('audio')):
            return None
        
        if 'content' in data['audio'] and 'format' in data['config']:
            audio = convert_and_save(data['audio']['content'], extension=data['config']['format'])
        else:
            return None

        itemoptions = STTInputItemOptions(data['config']['format'], audio)
        output_file = itemoptions.convert()
        
        return output_file
    
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


class STTInputItemOptions(object):
    def __init__(self, input_format, input_file):
        self.format = "wav"
        self.channels = 1
        self.bits = 16
        self.sample_rate = 16000
        self.encoding = "signed-integer"
        self.precision = "16-bit"
        self.bit_rate = "256k"

        self.input_format = input_format
        self.input_file = input_file
        self.output_file_path = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()) + ".wav")
        #self.output_file, self.output_file_path = tempfile.mkstemp(suffix=".wav")
    
    def parse_request(self, config):
        self.format = config.get("format", self.format)
        self.channels = config.get("channels", self.format)
        self.sample_rate = config.get("sample_rate", self.sample_rate)
        self.precision = config.get("precision", self.precision)
        self.bit_rate = config.get("bit_rate", self.bit_rate)

    def convert(self):
        tfm = sox.Transformer()
        #tfm.channels(1)
        #tfm.rate(16000)
        #tfm.convert(samplerate=16000, n_channels=1, bitdepth=16)
        tfm.set_input_format(file_type=self.input_format)
        tfm.set_output_format(file_type=self.format, rate=self.sample_rate, bits=self.bits, channels=self.channels, encoding=self.encoding)
        tfm.build(self.input_file, self.output_file_path)
        
        return self.output_file_path

