from flask import Flask, request, render_template, Response, jsonify, current_app, session
from util.converter import convertRawToB64Segments, convertRawToB64PSD
from werkzeug.utils import secure_filename
from tempfile import NamedTemporaryFile
import tempfile
from werkzeug.datastructures import FileStorage
import logging
import os
import threading
from mne.io import Raw
from pandas import DataFrame
from util.model import ModelHandler
import mne

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

MODEL_PATH = "lightgbm_model_trials_50.pkl"

# Shared variable
raw : Raw
df : DataFrame
sfreq : int
df_conversion_thread_event = threading.Event()
model_handler = ModelHandler(MODEL_PATH)

@app.route('/')
def home():
    # return Response("Hello World.", content_type="text/plain", status=200)
    return render_template('page/index.html') 

@app.route('/upload', methods=['POST'])
def upload_edf():    
    global filename
    global raw
    global sfreq
    global df
    
    edf_file = request.files["file"]
    bytes = edf_file.read()

    with NamedTemporaryFile(delete=False, suffix=".edf") as temp_file:
        temp_file.write(bytes)
        temp_file_path = temp_file.name
    filename = secure_filename(edf_file.filename)
    raw = mne.io.read_raw_edf(temp_file_path)
    raw = model_handler.clean_rename_channel(raw)
    sfreq = int(raw.info['sfreq'])
    
    if not raw.preload:
        raw.load_data()
    df = raw.to_data_frame()

    if 'edf' in session:
        try:
            os.remove(session['edf'])
        except FileNotFoundError:
            pass

    session['edf'] = temp_file_path
    return Response("Edf upload success. View EEG in 'View' tab.", content_type="text/plain", status=200)

@app.route('/view', methods=['GET'])
def view_eeg():
    global raw
    b64EegImages = convertRawToB64Segments(raw)
    b64PsdImage = convertRawToB64PSD(raw)
    response = {'eeg':b64EegImages, 'psd': b64PsdImage}
    return response

@app.route('/predict', methods=['GET', 'POST'])
def predict_seizure():
    try:
        prediction = model_handler.predict(raw)
        return jsonify({'prediction': prediction})
    except Exception:
        return jsonify({'error': Exception})

if __name__ == "__main__":
    app.run(debug=True)