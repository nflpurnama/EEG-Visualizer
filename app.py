from flask import Flask, request, render_template, Response, jsonify, current_app, session
from util.filemanager import createTempEdfFile
from util.converter import convertRawToB64, convertEdfToMneRaw
import logging
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

logging.basicConfig(filename='app.log', level=logging.DEBUG)

DEFAULT_EEG_START = 0
DEFAULT_EEG_END = 10
DEFAULT_VIEW_INTERVAL = 10

@app.route('/')
def home():
    return render_template('page/index.html') 

@app.route('/upload', methods=['POST'])
def upload_edf():    
    if 'edf' in session:
        os.remove(session['edf'])
    
    edf_file = request.files["file"]
    session['edf'] = createTempEdfFile(edf_file)
    current_app.current_raw = convertEdfToMneRaw(session['edf'])

    return Response("Edf upload success. View EEG in 'View' tab.", content_type="text/plain", status=200)
    #Save raw as session

@app.route('/view', methods=['GET'])
def view_edf():
    #obtain raw from session
    raw = current_app.current_raw
    #convert raw to image -- TODO: Explore client side rendering to send dataframe instead of image
    img_b64 = convertRawToB64(raw)

    return Response(img_b64, content_type='image/png')

@app.route('/navigate', methods=['POST'])
def navigate_timestamp():
    #obtain raw from session
    raw = current_app.current_raw
    timestamp = float(request.form['timestamp'])
    img_b64 = convertRawToB64(raw, timestamp)

    return Response(img_b64, content_type='image/png')

@app.route('/getdf', methods=['POST'])
def get_df():
    edf_file = request.files["file"]
    temp_file_path = createTempEdfFile(edf_file)
    df = convertEdfToDataFrame(temp_file_path)
    return jsonify(eeg_data=df.to_dict(orient='split'))

@app.route('/predict', methods=['POST'])
def predict_seizure():
    #TODO - run model from uploaded edf file
    return

if __name__ == "__main__":
    app.run(debug=True)