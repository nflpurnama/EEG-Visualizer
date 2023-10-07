import base64
import io
import mne
import matplotlib.pyplot as plt
import secrets
import os
import tempfile

def convert_edf_to_b64(edf_bytes):
    # Read the EEG data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as temp_file:
            temp_file.write(edf_bytes)
            temp_file_path = temp_file.name

    raw = mne.io.read_raw_edf(temp_file_path)
    raw = raw.pick_types(meg=False, eeg=True, eog=False, exclude='bads')
    
    # Plot the EEG data
    fig = raw.plot(show=False)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert BytesIO object to base64 string
    img_b64 = base64.b64encode(img.getvalue()).decode()
    
    # Delete temp file
    os.remove(temp_file_path)
    return img_b64