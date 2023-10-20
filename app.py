from flask import Flask, request, render_template, Response, jsonify, current_app, session
from util.filemanager import createTempEdfFile
from util.converter import convertRawToB64, convertEdfToMneRaw, convertRawToDataFrame
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

# Shared variable
raw : Raw
df : DataFrame
df_conversion_thread_event = threading.Event()

@app.route('/')
def home():
    return render_template('page/index.html') 

@app.route('/upload', methods=['POST'])
def upload_edf():    
    edf_file = request.files["file"]
    new_temp_file_path = createTempEdfFile(edf_file)
    
    global raw
    raw = convertEdfToMneRaw(new_temp_file_path)
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
def view_edf():
    #obtain raw from session
    global raw
    #convert raw to image -- TODO: Explore client side rendering to send dataframe instead of image
    img_b64 = convertRawToB64(raw)

    return Response(img_b64, content_type='image/png')

@app.route('/navigate', methods=['POST'])
def navigate_timestamp():
    #obtain raw from session
    global raw    
    timestamp = float(request.form['timestamp'])
    img_b64 = convertRawToB64(raw, timestamp)

    return Response(img_b64, content_type='image/png')

@app.route('/getdf', methods=['POST'])
def get_df():
    global df
    if df.empty:
        df_conversion_thread_event.wait()
        # return jsonify(eeg_data=df.to_dict(orient='split'))
    
    print(df.info())
    # Check memory usage of the DataFrame
    memory_usage = df.memory_usage(deep=True)

    # Print the memory usage for each column and the total memory usage
    print("Memory Usage for Each Column:")
    print(memory_usage)

    # Print the total memory usage
    print("Total Memory Usage:", memory_usage.sum())
    

@app.route('/predict', methods=['POST'])
def predict_seizure():
    #TODO - run model from uploaded edf file
    return

def rawToDataFrameThread(raw: Raw):
    global df
    df = convertRawToDataFrame(raw)

if __name__ == "__main__":
    app.run(debug=True)