# request digunakan untuk melakukan penggunaan metode HTTP seperti GET, POST, dll
from flask import Flask, render_template, request
# tensorflow.keras library untuk praproses
from tensorflow.keras.preprocessing.image import load_img, img_to_array
# tensorflow.keras library untuk menggunakan pretrained model
from tensorflow.keras.models import load_model
# untuk perhitungan komputasi
import numpy as np
# untuk regex pada string
import re
# pengaturan direktori
import os
# tanggalan
from datetime import date

today = date.today()

# dd/mm/YY
datefull = today.strftime("%d/%m/%Y")
datefull = str(datefull)
date_processed = datefull.split('/')
cur_year = date_processed[2]

# direktori model berada
loaded_model = load_model("models/hijaiyah.h5")
print('Model ready!!')

# inisialisasi flask
app = Flask(__name__)

import base64


# decoding an image from base64 into raw representation
def convertImage(imgData1):
    imgstr = re.search(r'base64,(.*)', str(imgData1)).group(1)
    with open('output.png', 'wb') as output:
        output.write(base64.b64decode(imgstr))

# load image
def load_image(img_path):
    # Praproses data uji
    img = load_img(img_path, target_size=(150,150,3))
    img_tensor = img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.0
    

    return img_tensor

@app.route('/')
def index():
    return render_template("index.html", year=cur_year)


@app.route('/predict/', methods=['GET', 'POST'])
def predict():
    class_names = [ 'ain', 'alif', 'ba', 'dal', 'dhod', 'dzal',
                'dzho', 'fa', 'ghoin', 'ha', 'ha\'', 'hamzah', 'jim',
                'kaf', 'kho', 'lam', 'lamalif', 'mim', 'nun', 'qof',
                'ro', 'shod', 'sin', 'syin', 'ta', 'tho', 'tsa', 
                'wawu', 'ya', 'zain']
    # ketika tombol prediksi ditekan maka akan dilakukan sebuah proses konversi berdasarkan yang dituliskan oleh pengguna
    imgData = request.get_data()
    # encode menjadi sebuah output.png
    convertImage(imgData)
    # membaca gambar
    img = load_image('output.png')

    # melakukan prediksi
    pred = loaded_model.predict(img)
    print(pred)
    print(class_names[np.argmax(pred)])
    # konversi respon menjadi string
    response = class_names[np.argmax(pred)]
    return str(response)


if __name__ == "__main__":
    # run the app locally 
    app.run(debug=False)