import numpy as np
import matplotlib.pyplot as plt
import base64
import mne
import io
from flask import Flask, request, jsonify, render_template

def mne_draw_web(folder, file):
    sample_edf = f'./dataset/physionet.org/files/siena-scalp-eeg/1.0.0/{folder}/{folder}-{file}.edf'
    
    # Read the EEG data
    raw = mne.io.read_raw_edf(sample_edf)
    raw = raw.pick_types(meg=False, eeg=True, eog=False, exclude='bads')
    
    # Plot the EEG data
    fig = raw.plot(show=False)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert BytesIO object to base64 string
    img_b64 = base64.b64encode(img.getvalue()).decode()

    # Close the Matplotlib figure to free up resources
    plt.close(fig)
    
    return render_template('page/index.html', eeg_plot=f'<img src="data:image/png;base64,{img_b64}" class="blog-image">')