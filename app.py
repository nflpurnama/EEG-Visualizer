from flask import Flask, request, render_template, Response
from util.filemanager import retrieveEdf
from util.generateimage import convertEdfToB64
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

logging.basicConfig(filename='app.log', level=logging.DEBUG)

@app.route('/')
def home():
    return render_template('page/index.html') 

@app.route('/view', methods=['POST'])
def view_edf():

    edf_file = request.files["file"]
    temp_file_path = retrieveEdf(edf_file)
    img_b64 = convertEdfToB64(temp_file_path)

    return Response(img_b64, content_type='image/png')

@app.route('/navigate', methods=['POST'])
def navigate_timestamp():
    timestamp = float(request.form['timestamp'])
    edf_file = request.files["file"]

    app.logger.debug(f"timestamp data type {type(timestamp)}")
    temp_file_path = retrieveEdf(edf_file)
    img_b64 = convertEdfToB64(temp_file_path, start=timestamp)

    return Response(img_b64, content_type='image/png')

@app.route('/predict', methods=['POST'])
def predict_seizure():
    #TODO - run model from uploaded edf file
    return

if __name__ == "__main__":
    app.run(debug=True)