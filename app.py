from flask import Flask, render_template, Response, send_file, jsonify, make_response
import cv2
import os
import io
from base64 import b64encode
from run import run
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array,load_img

app = Flask(__name__)

def gen_frame(begin): 
    global camera
    if begin == 1:
        while begin == 1:
            run()
    else:
        print()

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

@app.route("/")
def index():
    return render_template('home.html', begin=0, capture_btn = False, captured_img = None)

@app.route("/start_video", methods=["POST","GET"])
def start_video():
    return render_template('home.html', begin = 1, capture_btn = True, captured_img = None)

@app.route('/video_feed/<int:begin>', methods=["POST","GET"])
def video_feed(begin):
    return Response(gen_frame(begin), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/end_video', methods=["POST","GET"])
def end_video():
    return render_template('home.html', begin= 0, capture_btn = False, captured_img = None)

app.config["CACHE_TYPE"] = "null"
@app.route('/capture', methods=["POST", "GET"])
def capture():
    global frame
    #print(frame, frame.shape)
    cv2.imwrite('./static/captured.jpg', frame)
    image_bn = open('./static/captured.jpg', 'rb').read()
    image = b64encode(image_bn).decode('utf-8')
    return jsonify({'status':1, 'image': image})


@app.route('/delete_img', methods=["POST", "GET"])
def delete_img():
    os.remove("./static/captured.jpg")
    return render_template('home.html', begin = 1, capture_btn = True, captured_img = None)

@app.route('/retry', methods=['POST', 'GET'])
def retry():
    os.remove("./static/captured.jpg")
    os.remove("./static/pred_img.jpg")
    return render_template('home.html', begin = 1, capture_btn = True, captured_img = None)

app.run(debug=True)
