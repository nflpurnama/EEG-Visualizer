import base64
import io
import mne
import matplotlib.pyplot as plt
import secrets
import os
import tempfile
from datetime import time

def convert_edf_to_b64(edf_bytes, start=0.0):
    if isinstance(start, str):
          hours, minutes, seconds = map(int, start.split(':'))
          start = hours * 3600 + minutes * 60 + seconds
    
    elif isinstance(start, time):
          start = start.hour * 3600 + start.minute * 60 + start.second

    # Read the EEG data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".edf") as temp_file:
            temp_file.write(edf_bytes)
            temp_file_path = temp_file.name

    raw = mne.io.read_raw_edf(temp_file_path)
    raw = raw.pick_types(meg=False, eeg=True, eog=False, exclude='bads')
    
    # Plot the EEG data
    fig = raw.plot(show=False, start=start)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Convert BytesIO object to base64 string
    img_b64 = img.getvalue()
    
    # Delete temp file
    os.remove(temp_file_path)
    return img_b64