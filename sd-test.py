import pyaudio

def find_input_devices():
    pa = pyaudio.PyAudio()
    for i in range(pa.get_device_count()):
        devinfo = pa.get_device_info_by_index(i)
        print("Device %d: %s" % (i, devinfo["name"]))

audio_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
								channels=2,
								rate=44100,
								input=True,
								# Uncomment and set this using find_input_devices.py
								# if default input device is not correct
								#input_device_index=2, \
								frames_per_buffer=1024)

find_input_devices()

