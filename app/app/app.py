import os
import uuid
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Dossier d'upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Charger le modèle softmax
model = tf.keras.models.load_model('model/model.keras')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        file = request.files['image']
        if file:
            # Générer un nom unique
            filename = f"{uuid.uuid4().hex}_{file.filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Prétraitement de l’image
            image = Image.open(filepath).convert('RGB')
            image = image.resize((64, 64))
            img_array = np.array(image) / 255.0
            img_array = img_array.reshape(1, 64, 64, 3)

            # Prédiction
            prediction = model.predict(img_array)
            pred_class = np.argmax(prediction[0])  # ⚠️ Softmax à 2 classes

            if pred_class == 1:
                result = "Zone touchée par la sécheresse"
            else:
                result = "Zone non touchée"

            return render_template('analyze.html', image=filename, result=result, loading=False)

    return render_template('analyze.html', image=None, result=None, loading=False)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
