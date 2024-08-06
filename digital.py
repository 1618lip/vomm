import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.signal import butter, lfilter
from matplotlib.widgets import Slider

# Generate a fixed signal (sine wave)
def generate_sine_wave(freq, sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return t, np.sin(2 * np.pi * freq * t)

# Generate a random signal
def generate_random_signal(sample_rate, duration):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    return t, np.random.randn(len(t))

# Design a Butterworth filter
def butter_filter(cutoff, fs, order=5, btype='low'):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
    return b, a

# Apply the filter to a signal
def apply_filter(data, b, a):
    return lfilter(b, a, data)

# Initialize the figure and axes
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Generate signals
sample_rate = 1000
duration = 5.0
t_sine, sine_wave = generate_sine_wave(50, sample_rate, duration)
t_random, random_signal = generate_random_signal(sample_rate, duration)

# Design filters
lowcut = 100.0
order = 6
b_low, a_low = butter_filter(lowcut, sample_rate, order, btype='low')

# Initialize lines for plotting
line1, = ax1.plot([], [], label='Filtered Sine Wave', linestyle='--')
line2, = ax2.plot([], [], label='Filtered Random Signal', linestyle='--')
ax1.set_xlim(0, duration)
ax1.set_ylim(-1.5, 1.5)
ax2.set_xlim(0, duration)
ax2.set_ylim(-3, 3)
ax1.legend()
ax2.legend()
ax1.grid()
ax2.grid()

# Update function for animation
def update(frame):
    filtered_sine = apply_filter(sine_wave[:frame], b_low, a_low)
    filtered_random = apply_filter(random_signal[:frame], b_low, a_low)
    
    line1.set_data(t_sine[:frame], filtered_sine)
    line2.set_data(t_random[:frame], filtered_random)
    
    return line1, line2

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(t_sine), blit=True, interval=10, repeat=False)

# Create sliders for interactive control
axcolor = 'lightgoldenrodyellow'
axcutoff = plt.axes([0.15, 0.01, 0.65, 0.03], facecolor=axcolor)

scutoff = Slider(axcutoff, 'Cutoff', 10.0, 500.0, valinit=lowcut)

# Update function for slider
def update_slider(val):
    global b_low, a_low
    cutoff = scutoff.val
    b_low, a_low = butter_filter(cutoff, sample_rate, order, btype='low')
    ani.event_source.start()

scutoff.on_changed(update_slider)

plt.show()
