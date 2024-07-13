import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mne
from mne.io import Raw
import os
import base64

def convertRawToB64Segments(raw):
    duration = 5.0
    b64Images = []
    for i in range(0, int(raw.times[-1])+1, int(duration)):
        raw.plot(duration=duration, start=i, scalings={'eeg':5e-5})
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        b64Image = base64.b64encode(img.getvalue()).decode('utf-8')
        b64Images.append(b64Image)
    return b64Images

def convertRawToB64PSD(raw):
    raw.compute_psd().plot()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    b64Image = base64.b64encode(img.getvalue()).decode('utf-8')
    return b64Image