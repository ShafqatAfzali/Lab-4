import nidaqmx
from nidaqmx import constants
from nidaqmx import stream_readers
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt

MYDAQ = "myDAQ2"
CHANNEl = "ai0"
fs = 8000
måling_tid = 2
plotting_tid = 0.3
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

    start = 0
    end = antall_plott_samples

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
    plt.show()
