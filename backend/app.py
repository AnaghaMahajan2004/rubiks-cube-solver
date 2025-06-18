import os
import numpy as np
import cv2
import json
from flask import Flask, render_template, request, send_from_directory, session, redirect, url_for
from tensorflow.keras.models import load_model
import kociemba
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret_key_here'

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
MODEL_PATH = os.path.join(BASE_DIR, 'model/color_classifier.keras')
CLASS_INDEX_PATH = os.path.join(BASE_DIR, 'model/class_indices.json')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load model and class map
model = load_model(MODEL_PATH)
with open(CLASS_INDEX_PATH, 'r') as f:
    class_indices = json.load(f)
idx_to_label = {v: k.capitalize() for k, v in class_indices.items()}


def generate_cube_string(cube_faces):
    from collections import Counter
    face_centers = {face: colors[4] for face, colors in cube_faces.items()}
    if len(set(face_centers.values())) != 6:
        raise ValueError("Face centers must be unique.")
    face_order = ['U', 'R', 'F', 'D', 'L', 'B']
    color_to_face_letter = {color: face for face, color in face_centers.items()}
    cube_string = ''
    for face in face_order:
        for color in cube_faces[face]:
            if color not in color_to_face_letter:
                raise ValueError(f"Unknown color '{color}' in face data.")
            cube_string += color_to_face_letter[color]
    return cube_string


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'cube_image' not in request.files:
            return 'No file part'
        file = request.files['cube_image']
        if file.filename == '':
            return 'No selected file'
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        img = cv2.imread(filepath)
        h, w, _ = img.shape
        min_dim = min(h, w)
        start_x = (w - min_dim) // 2
        start_y = (h - min_dim) // 2
        img = img[start_y:start_y + min_dim, start_x:start_x + min_dim]
        img = cv2.resize(img, (300, 300))

        face_colors = []
        step = 100
        for row in range(3):
            row_colors = []
            for col in range(3):
                x, y = col * step, row * step
                facelet = img[y:y + step, x:x + step]
                avg_color = facelet.mean(axis=(0, 1)).astype(np.uint8)
                patch = np.ones((32, 32, 3), dtype=np.uint8) * avg_color
                patch = cv2.cvtColor(patch, cv2.COLOR_BGR2RGB) / 255.0
                patch = np.expand_dims(patch, axis=0)
                prediction = model.predict(patch, verbose=0)
                predicted_class = np.argmax(prediction)
                predicted_color = idx_to_label.get(predicted_class, 'Unknown')
                row_colors.append(predicted_color)
            face_colors.append(row_colors)

        face_id = request.form.get('face_id')
        cube_faces = session.get('cube_faces', {})
        cube_faces[face_id] = sum(face_colors, [])
        session['cube_faces'] = cube_faces

        return render_template('index.html', uploaded=True, filename=filename, face_colors=face_colors)

    return render_template('index.html', uploaded=False)


@app.route('/solve', methods=['POST'])
def solve():
    if 'cube_faces' not in session or len(session['cube_faces']) != 6:
        return redirect('/')
    cube_faces = session['cube_faces']
    cube_string = generate_cube_string(cube_faces)
    solution = kociemba.solve(cube_string).split()
    scramble = kociemba.solve(cube_string)  # Treat solution as scramble for twisty-player
    return render_template("solution.html", cube_string=cube_string, solution=solution, scramble=scramble)


@app.route('/reset', methods=['POST'])
def reset():
    session.pop('cube_faces', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.run(debug=True)
