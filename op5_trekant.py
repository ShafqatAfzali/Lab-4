import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

t = np.arange(0, 5, 0.01)
N_MAX = 5
T = 1


def fourierSeries(n_max, t):
    partialSums = 0
    for n in range(1, n_max):
        try:
            bn = 8/(np.pi*(2*n-1))**2
            wn = 2*np.pi*(2*n-1)/T
            partialSums = partialSums + bn*np.cos(wn*t)
        except:
            print("pass")
            pass
    return partialSums


f = fourierSeries(N_MAX, t)

plt.style.use("ggplot")
plt.plot(t, signal.sawtooth(2*np.pi*(1/T)*t-np.pi,
         width=0.5), color="blue", label="Signal")
plt.plot(t, f, 'r--', label="Fourierserie-approksimasjon")
plt.xlabel('t[s]')
plt.title("Fourierserie-approksimasjon med antall ledd = "+str(N_MAX))
plt.legend(loc=1)
plt.tight_layout()
plt.show()
