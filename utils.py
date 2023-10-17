import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# from seizure_detection.load import data_load
# from seizure_detection.instantiatemne import mne_object
from seizure_detection.filemanager import retrieveEdf
import mne
import os

def convertEdfToB64(file, start=0.0):

    # Read the EEG data
    # df, freq = data_load(file)
    # raw = mne_object(df, freq)

    temp_file_path = retrieveEdf(file)
    raw = mne.io.read_raw_edf(temp_file_path)
    raw = raw.pick_types(meg=False, eeg=True, eog=False, exclude='bads')
    
    duration = raw.n_times / raw.info['sfreq']
    if start > duration:
        start = 0
    
    plot_kwargs = {
        'scalings': dict(eeg=20e-5),   # zooms the plot out
        'highpass': 0.5,              # filters out low frequencies
        'lowpass': 70.,                # filters out high frequencies
    }
    # Plot the EEG data
    fig = raw.plot(show=False, start=start, **plot_kwargs)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert BytesIO object to base64 string
    img_b64 = img.getvalue()
    
    return img_b64