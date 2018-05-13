# Credit to Will Yager

import pyaudio as pa
import numpy as np
import notes_noscaled_nosaturation

deviceCount = pa.PyAudio().get_device_count()
audio_stream = None

def init(channel=-1):
    global audio_stream
    if channel > -1:
        audio_stream = pa.PyAudio().open(format=pa.paInt16,
                                     channels=2,
                                     rate=44100,
                                     input=True,
                                     input_device_index=channel,
                                     frames_per_buffer=1024)
    else:
        audio_stream = pa.PyAudio().open(format=pa.paInt16,
                                         channels=2,
                                         rate=44100,
                                         input=True,
                                         frames_per_buffer=1024)

# Convert the audio data to numbers, num_samples at a time.
def read_audio(audio, num_samples):
    while True:
        # Read all the input data.
        samples = audio.read(num_samples)
        # Convert input data to numbers
        samples = np.fromstring(samples, dtype=np.int16).astype(np.float)
        samples_l = samples[::2]
        samples_r = samples[1::2]
        yield (samples_l, samples_r)


def visualizeAudio():
    audio = read_audio(audio_stream, num_samples=512)
    return notes_noscaled_nosaturation.fft(audio)