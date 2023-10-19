import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mne

def convertEdfToB64(file_path: str, start=0.0):
    raw = mne.io.read_raw_edf(file_path)
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

def convertEdfToMneRaw(file_path: str):
    raw = mne.io.read_raw_edf(file_path)
    return raw