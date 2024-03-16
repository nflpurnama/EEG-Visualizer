from flask import Flask, request, render_template, Response, jsonify, current_app, session
from util.filemanager import createTempEdfFile
from util.converter import convertRawToB64, convertEdfToMneRaw, convertRawToDataFrame
from util.cleaner import clean_rename_channel
import logging
import os
import threading
from mne.io import Raw
from pandas import DataFrame

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

logging.basicConfig(filename='app.log', level=logging.DEBUG)

DEFAULT_EEG_START = 0
DEFAULT_EEG_END = 10
DEFAULT_VIEW_INTERVAL = 10
DEFAULT_USE_CHANNELS = ['Fp1', 'Fp2', 'F3', 'F4', 'C3', 'C4', 'P3', 'P4', 'O1', 'O2', 'F7', 'F8', 'T7','T8','P7','P8','P9','P10', 'Fz', 'Cz', 'Pz','F9','F10','T9','T10']

# Shared variable
raw : Raw
df : DataFrame
sfreq : int
df_conversion_thread_event = threading.Event()

@app.route('/')
def home():
    return render_template('page/index.html') 

@app.route('/upload', methods=['POST'])
def upload_edf():    
    edf_file = request.files["file"]
    new_temp_file_path = createTempEdfFile(edf_file)
    
    global raw
    raw = clean_rename_channel(convertEdfToMneRaw(new_temp_file_path), DEFAULT_USE_CHANNELS)
    global sfreq
    sfreq = int(raw.info['sfreq'])

    rawToDataFrameThread(raw)
    # process_thread = threading.Thread(target=rawToDataFrameThread, args=(raw))
    # process_thread.start()
    # print("THREAD STARTED")
    # df_conversion_thread_event.set()

    if 'edf' in session:
        try:
            os.remove(session['edf'])
        except FileNotFoundError:
            pass

    session['edf'] = new_temp_file_path
    return Response("Edf upload success. View EEG in 'View' tab.", content_type="text/plain", status=200)
    #Save raw as session

@app.route('/view', methods=['GET'])
def view_eeg():
    global df
    global sfreq
    len = DEFAULT_EEG_END * sfreq
    transposed_df = df.T
    row_dict = {index: values.tolist() for index, values in transposed_df.iterrows()}
    # Return the JSON object as a response
    return jsonify(row_dict)

@app.route('/viewdf', methods=['GET'])
def view_df():
    global df
    global sfreq
    len = DEFAULT_EEG_END * sfreq
    temp_df = df.T
    return render_template('view_data.html', table=temp_df.to_html())


@app.route('/navigate', methods=['POST'])
def navigate_timestamp():
    #TODO - navigate to section of video
    return

@app.route('/getdf', methods=['POST'])
def get_df():
    start = request.form.get('start')
    end = request.form.get('end')

    global sfreq
    start_idx = int(sfreq * start)
    end_idx = int(sfreq * end)

    #TODO - get dataframe data
    global df
    paginated_data = df.iloc[0:5000, 1].to_json()  # Convert DataFrame to a list of dictionaries
    return jsonify(paginated_data)
    

@app.route('/predict', methods=['POST'])
def predict_seizure():
    #TODO - run model from uploaded edf file
    return

def rawToDataFrameThread(raw: Raw):
    global df
    df = convertRawToDataFrame(raw)

if __name__ == "__main__":
    app.run(debug=True)