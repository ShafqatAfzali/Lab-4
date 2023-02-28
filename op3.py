import nidaqmx
from nidaqmx import constants
from nidaqmx import stream_readers
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

MYDAQ = "myDAQ2"
CHANNEl = "ai0"
fs = 190000  # (max fs =200KHz for myDAQ)
måling_tid = 1
plotting_tid = 0.01  # (juster slik at man ser periodistet når sdet gjelder)
antall_samples = int(måling_tid*fs)
samples_per_kanal = antall_samples
antall_plott_samples = int(plotting_tid*fs)

with nidaqmx.Task() as mål:
    mål._ai_channels.add_ai_voltage_chan(
        physical_channel=MYDAQ+"/"+CHANNEl)

    mål.timing.cfg_samp_clk_timing(
        rate=fs, sample_mode=constants.AcquisitionType.CONTINUOUS, samps_per_chan=samples_per_kanal)

    opptak = stream_readers.AnalogMultiChannelReader(mål.in_stream)

    sample_vekt = np.zeros([1, antall_samples])
    mål.start()
    opptak.read_many_sample(
        data=sample_vekt, number_of_samples_per_channel=antall_samples, timeout=-1)

    ren_sample_vekt = sample_vekt[0]-np.mean(sample_vekt[0])
    xx = np.linspace(0, antall_samples/fs, antall_samples)

    interp_yy = interp1d(xx, ren_sample_vekt, kind="cubic")
    final_xx = np.linspace(0, antall_samples/fs, antall_samples*10)
    final_yy = interp_yy(final_xx)

    plt.subplot(121)
    start = int(np.floor(antall_samples/5))
    end = int(start+antall_plott_samples)

    if end > antall_samples:
        end = antall_samples

    plt.plot(xx[start:end], ren_sample_vekt[start:end],
             ".", ms=6, label="samplinger")
    plt.plot(final_xx[start*10:end*10],
             final_yy[start*10:end*10], label="cubic interpolation")
    plt.xlabel("tid [sek]")
    plt.ylabel("amplitude [Volt]")
    plt.legend(loc="upper right")
    plt.grid()

    plt.subplot(122)
    frekvens = plt.magnitude_spectrum(
        ren_sample_vekt, Fs=fs, Fc=0, sides="onesided")
    plt.xlabel("frekvens [Hz]")
    plt.ylabel("amplitude [Volt]")
    plt.grid()
    plt.plot()
    plt.xlim(0, 6000)
    plt.tight_layout()

    for index, amplitude in enumerate(frekvens[0]):
        if amplitude > 0.007:
            print(frekvens[1][index], amplitude)

    plt.show()
