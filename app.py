import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify, render_template
from forms import upload_edf_form
from utils import convert_edf_to_b64
import io
import os
import tempfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any secret string'

@app.route('/viewer', methods=["GET", "POST"])
def viewer():
    form = upload_edf_form()

    # Render HTML with base64 image
    if form.validate_on_submit():
        edf_file = request.files["edf_file"]
        edf_bytes = edf_file.read()
        img_b64 = convert_edf_to_b64(edf_bytes)
        html = f'<img src="data:image/png;base64,{img_b64}" class="blog-image">'
        return render_template('page/index.html', eeg_plot=html, form=form)
    
    else:
        return render_template('page/index.html', form=form)    

if __name__ == "__main__":
    app.run(debug=True)