from flask import Flask, request, render_template, Response
from utils import convert_edf_to_b64
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
    edf_bytes = edf_file.read()
    img_b64 = convert_edf_to_b64(edf_bytes=edf_bytes)

    return Response(img_b64, content_type='image/png')

@app.route('/navigate', methods=['POST'])
def navigate_timestamp():
    timestamp = float(request.form['timestamp'])
    edf_file = request.files["file"]

    app.logger.debug(f"timestamp data type {type(timestamp)}")

    edf_bytes = edf_file.read()
    img_b64 = convert_edf_to_b64(edf_bytes=edf_bytes, start=timestamp)

    return Response(img_b64, content_type='image/png')

if __name__ == "__main__":
    app.run(debug=True)