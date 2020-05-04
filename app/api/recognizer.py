import os
from flask import current_app

from kaldi.asr import GmmLatticeFasterRecognizer
from kaldi.decoder import LatticeFasterDecoderOptions
from kaldi.feat.mfcc import Mfcc, MfccOptions
from kaldi.feat.functions import compute_deltas, DeltaFeaturesOptions
from kaldi.feat.window import FrameExtractionOptions
from kaldi.transform.cmvn import Cmvn
from kaldi.util.table import SequentialMatrixReader, SequentialWaveReader

class SpeechRecognizer:
    """
    This class create a recognizer and give the
    possibility to make speech recognition from wav files.
    """
    def __init__(self, base_path=None, model_path=None, graph_path=None, symbols_path=None):
        # Declaring main variables
        self.base_path = current_app.config.get('ASR_BASE')
        self.model_path = model_path or current_app.config['ASR_MODEL_PATH']
        self.graph_path = graph_path or current_app.config['ASR_GRAPH_PATH']
        self.symbols_path = graph_path or current_app.config['ASR_SYMBOLS_PATH']

        # recognizer
        self.asr = self.create_recognizer()
        self.feat_pipeline = self.get_feat_pipeline()

    def create_recognizer(self, decoder_opts=None):
        """
        Create a GmmLatticeFasterRecognizer
        :return: recognizer object
        """
        if decoder_opts is not None:
            decoder_opts = decoder_opts
        else:
            decoder_opts = LatticeFasterDecoderOptions()
            decoder_opts.beam = 13.0
            decoder_opts.max_active = 7000
        self.asr = GmmLatticeFasterRecognizer.from_files(
        self.model_path, self.graph_path, self.symbols_path, decoder_opts=decoder_opts)
        
        return self.asr

    def recognize(self, filepath=None):
        result = None

        # Create a tmp wav.scp file
        wav_scp_path = os.path.join(os.path.dirname(filepath), "wav.scp")
        with open(wav_scp_path, "w") as f:
            f.write("unknown %s" % filepath)
        # Decode

        for key, wav in SequentialWaveReader("scp:%s" % wav_scp_path):
            feats = self.feat_pipeline(wav)
            out = self.asr.decode(feats)
            result = out["text"]
        return result
    
    def get_feat_pipeline(self):
        """
        Instanciate a pipeline for the recognizer
        """
        frame_opts = FrameExtractionOptions()
        frame_opts.samp_freq = 16000
        frame_opts.allow_downsample = True
        mfcc_opts = MfccOptions()
        mfcc_opts.use_energy = False
        mfcc_opts.frame_opts = frame_opts
        self.feat_pipeline = self.make_feat_pipeline(Mfcc(mfcc_opts))

        return self.feat_pipeline

    @staticmethod
    def make_feat_pipeline(base, opts=DeltaFeaturesOptions()):
        """
        Create a pipeline for the recognizer from opts
        """
        def feat_pipeline(wav):
            feats = base.compute_features(wav.data()[0], wav.samp_freq, 1.0)
            cmvn = Cmvn(base.dim())
            cmvn.accumulate(feats)
            cmvn.apply(feats)
            return compute_deltas(opts, feats)
        return feat_pipeline
