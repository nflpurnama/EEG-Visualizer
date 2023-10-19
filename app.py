from flask import Flask, request, render_template, Response, jsonify, session
from util.filemanager import createTempEdfFile
from util.generateimage import convertEdfToB64, convertEdfToMneRaw
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('page/index.html') 

@app.route('/upload', methods=['POST'])
def upload_edf():
    edf_file = request.files["file"]
    temp_file_path = createTempEdfFile(edf_file)
    raw = convertEdfToMneRaw(temp_file_path)
    session['raw'] = raw
    #Save raw as session

@app.route('/view', methods=['POST'])
def view_edf():
    #obtain raw from session
    #trim a copy of raw
    #convert copy to dataframe
    edf_file = request.files["file"]
    temp_file_path = createTempEdfFile(edf_file)
    img_b64 = convertEdfToB64(temp_file_path)

    return Response(img_b64, content_type='image/png')

@app.route('/navigate', methods=['POST'])
def navigate_timestamp():
    #obtain raw from session
    #trim a copy of raw based on timestamp requested
    #convert copy to dataframe
    timestamp = float(request.form['timestamp'])
    edf_file = request.files["file"]

    app.logger.debug(f"timestamp data type {type(timestamp)}")
    temp_file_path = createTempEdfFile(edf_file)
    img_b64 = convertEdfToB64(temp_file_path, start=timestamp)

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