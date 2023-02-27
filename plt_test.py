import time
import matplotlib.pyplot as plt
import numpy as np
from numpy.random import rand

if __name__ == '__main__':
    # Enable interactive mode.
    plt.ion()
    # Create a figure and a set of subplots.
    figure, ax = plt.subplots()
    # return AxesImage object for using.
    lines, = ax.plot([], [])
    ax.set_autoscaley_on(True)
    ax.set_ylim(0, 1)
    ax.grid()
    for n in range(600):
        # A template of data generate...
        xdata = np.arange(128)
        ydata = rand(128)

        # update x, y data
        lines.set_xdata(xdata)
        lines.set_ydata(ydata)
        #Need both of these in order to rescale
        ax.relim()
        ax.autoscale_view()
        # draw and flush the figure .
        figure.canvas.draw()
        figure.canvas.flush_events()
        time.sleep(0.01) 