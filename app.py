import numpy as np
import matplotlib.pyplot as plt
import base64
import mne
import io
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/plot')
def mne_read_raw_save_draw():
    
    eeg_folder = request.args.get('folder', default=None)
    
    if eeg_folder is None:
        return "Please provide a 'folder' query parameter to specify the EEG data file.", 400
    
    eeg_file = request.args.get('file', default=None)
    
    if eeg_file is None:
        return "Please provide a 'file' query parameter to specify the EEG data file.", 400
    
    
    sample_edf = f'./dataset/physionet.org/files/siena-scalp-eeg/1.0.0/{eeg_folder}/{eeg_folder}-{eeg_file}.edf'
    
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

    # Render HTML with base64 image
    html = f'<img src="data:image/png;base64,{img_b64}" class="blog-image">'
    return render_template('page/index.html', eeg_plot=f'<img src="data:image/png;base64,{img_b64}" class="blog-image">')
    


if __name__ == "__main__":
    app.run(debug=True)
