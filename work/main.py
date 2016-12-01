from flask import Flask, request, redirect, flash, jsonify
import cv2
import numpy as np
import dlib

# 顔の検出に利用
detector = dlib.get_frontal_face_detector()
# 顔のパーツの検出に利用
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# predictorが返す68個の点の構成を定義
PARTS = {
    'contour': range(0, 17),
    'eyebrow_right': range(17, 22),
    'eyebrow_left': range(22, 27),
    'nose': range(27, 36),
    'eye_right': range(36, 42),
    'eye_left': range(42, 48),
    'mouth': range(48, 68)
}

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    '''
    顔の検出を簡単に試す、画像アップロードフォームのページです。
    '''
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        data = np.asarray(bytearray(file.read()), dtype=np.uint8)
        image = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return jsonify(__detect_faces(image))
    return '''
    <!doctype html>
    <title>Detect Face Shape</title>
    <p>Upload an image file to detect the face shape.</p>
    <form action='' method=post enctype=multipart/form-data>
      <p><input type='file' name='file'>
         <input type='submit' value='Upload'>
    </form>
    '''

@app.route("/detect", methods=['POST'])
def detect_faces():
    '''
    HTTPリクエストボディのバイナリを画像として読み込み、顔を検出してjsonで返します。
    '''
    data = np.asarray(bytearray(request.get_data()), dtype=np.uint8)
    image = cv2.imdecode(data, cv2.IMREAD_COLOR)
    return jsonify(__detect_faces(image))

def __detect_faces(image):
    '''
    与えられた画像から複数の顔を検出し、顔のそれぞれのパーツの座標を返します。
    '''
    dets = detector(image, 1)
    faces = []
    for k, d in enumerate(dets):
        shape = predictor(image, d)
        parts = {}
        for name, pointrange in PARTS.items():
            part = []
            for i in list(pointrange):
                p = shape.part(i)
                part.append({'x': p.x, 'y': p.y})
            parts[name] = part

        left, right, top, bottom = 100000, 0, 100000, 0
        for part in shape.parts():
            left = min(left, part.x)
            right = max(right, part.x)
            top = min(top, part.y)
            bottom = max(bottom, part.y)

        face = {}
        face['bounds'] = {
            'x': left,
            'y': top,
            'width': right - left,
            'height': bottom - top
        }
        face['parts'] = parts
        faces.append(face)
    return faces

app.debug = True
app.run(host='0.0.0.0')
