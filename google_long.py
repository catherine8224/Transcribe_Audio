from google.cloud import speech_v1
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1 import enums
import io
import os
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/catherineng/Downloads/My Project 52130-da00a565db68.json"


def sample_long_running_recognize(storage_uri):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    #client = speech_v1.SpeechClient()
    client = speech_v1p1beta1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # The number of channels in the input audio file (optional)
    audio_channel_count = 1

    # When set to true, each audio channel will be recognized separately.
    # The recognition result will contain a channel_tag field to state which
    # channel that result belongs to
    enable_separate_recognition_per_channel = True

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100#16000

    # The language of the supplied audio
    language_code = "en-US"


    # Specify up to 3 additional languages as possible alternative languages
    # of the supplied audio.
    alternative_language_codes_element = "es-MX"
    alternative_language_codes_element_2 = "fr-FR"
    alternative_language_codes = [
        alternative_language_codes_element,
        alternative_language_codes_element_2,
    ]

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "audio_channel_count": audio_channel_count,
        "enable_separate_recognition_per_channel": enable_separate_recognition_per_channel,
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        #"alternative_language_codes": alternative_language_codes,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    stored_data = []
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        #print(type(alternative)) #<class 'google.cloud.speech_v1.types.SpeechRecognitionAlternative'> #None   #<class 'google.cloud.speech_v1.types.SpeechRecognitionAlternative'>
        alternatives = alternative.transcript
        #print(type(alternatives))
        stored_data.append(alternatives)
        data = ' '.join(stored_data[::2])
        #alternative = alternative.transcript
        #print("RESULT: " , result)
        #print("Alternative: ", alternative)
        #print(u"Transcript: {}".format(alternative.transcript))
    return data


#print(type(sample_long_running_recognize("gs://awesome-bucketness/peacocks.wav")))