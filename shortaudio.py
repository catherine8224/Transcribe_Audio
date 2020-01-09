from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import re

from pydub import AudioSegment
    

def sample_recognize(storage_uri):
    """
    Transcribe short audio file from Cloud Storage using synchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    #storage_uri = 'gs://staging.striking-scout-263519.appspot.com/transcript.mp3'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    
    #encoding = enums.RecognitionConfig.AudioEncoding.MP3
    #encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED

    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    response = client.recognize(config, audio)
    #print(response.results)
    #wordbank = []
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        #alternative = str(alternative)
        #word = re.split(r'\s+', alternative)
        #print(word[4])
        #print(alternative)
        print(u"Transcript: {}".format(alternative.transcript))
#gs://[mybucket]/[myfile]
#gs://staging.striking-scout-263519.appspot.com/transcript.mp3

# def main():
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "--storage_uri",
#         type=str,
#         default="gs://awesome-bucketness/output5.wav",
#     )
#     args = parser.parse_args()

#     sample_recognize(args.storage_uri)


if __name__ == "__main__":
    main()