import pyaudio
import wave

import numpy as np
from matplotlib import pyplot as plt
import struct

import time

filename = f"./voiceData/breathy_voice.wav"
plt.ion()# Create a figure and a set of subplots.
figure, ax = plt.subplots()# return AxesImage object for using.
lines, = ax.plot([], [])
ax.set_autoscaley_on(True)
ax.set_ylim(0, 1)
ax.grid()
    
xdata = np.linspace(0,1023)


def callback(in_data, frame_count, time_info, status):

    ydata = np.frombuffer(in_data, dtype=np.int16)

    # lines.set_xdata(xdata)
    # lines.set_ydata(ydata)
    # #Need both of these in order to rescale
    # ax.relim()
    # ax.autoscale_view()
    # # draw and flush the figure .
    figure.canvas.draw()
    figure.canvas.flush_events()

    return (in_data, pyaudio.paContinue)

  
p = pyaudio.PyAudio()


stream = p.open(
                    format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    output=True,
                    input=True,
                    frames_per_buffer=1024,
                    stream_callback=callback
                )

while stream.is_active() :
    time.sleep(0.1)

    # Close the stream (5)
stream.close()

    # Release PortAudio system resources (6)
p.terminate()