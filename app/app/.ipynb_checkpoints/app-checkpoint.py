from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# تأكدي من وجود المجلد اللي غادي تخزني فيه الصور
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def predict_drought(image_path):
    # دالة مؤقتة للتجربة
    if 'dry' in image_path.lower():
        return "Drought detected"
    else:
        return "No drought detected"

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            result = predict_drought(filepath)
            return render_template('index.html', result=result, filename=file.filename)
    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)
