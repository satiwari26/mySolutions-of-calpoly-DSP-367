import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter

# Define filter coefficients
r1 = 0.9
b0 = [1, -r1, 0]
a = [1, -2*r1*np.cos(2*np.pi*697/4000), r1*r1]

# Generate input signal
n = np.arange(0, 1000)
xin = np.sin(2*np.pi*1000/4000*n) + np.sin(2*np.pi*2000/4000*n)

# Apply filter using lfilter function
yout = lfilter(b0, a, xin)

# Plot input and output signals
plt.plot(n, xin, label='Input')
plt.plot(n, yout, label='Output')
plt.legend()
plt.xlabel('Sample')
plt.ylabel('Amplitude')
plt.show()