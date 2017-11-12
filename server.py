from flask import Flask, request, send_from_directory, send_file, jsonify
import sys
sys.path.insert(0, 'src')
import transform, numpy as np, vgg, pdb, os
import tensorflow as tf
import evaluate_style
import analyze_image
import cv2
import os

app = Flask(__name__)

out_file = "./result.png"
in_file = "./to_stylize.png"
all_styles = ["./styles/la_muse.ckpt","./styles/rain_princess.ckpt","./styles/scream.ckpt","./styles/udnie.ckpt","./styles/wave.ckpt"]

@app.route("/get_analysis", methods=['GET', 'POST'])
def analyse():
    print("analyse image")
    im_name = "analyze.png"
    file = request.files.get('file', '')
    f = open(im_name, 'wb')
    f.write(file.read())
    f.close()
    s = analyze_image.analysis(im_name)
    return s

@app.route("/style", methods=['GET', 'POST'])
def picStylize():
    print("stylize image")
    print(request.form)
    index = int(request.form['num'])
    file = request.files.get('file', '')
    print(index)
    f = open(in_file, 'wb')
    f.write(file.read())
    f.close()

    im = cv2.imread(in_file)
    im = cv2.resize(im, (600,600))
    (h, w) = im.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, -90, 1.0)
    im = cv2.warpAffine(im, M, (w, h))
    cv2.imwrite(in_file, im)

    try:
        os.removedirs("./results")
    except:
        pass

    # style_name = np.random.choice(all_styles)
    style_name = all_styles[index]
    print("Using ",style_name)
    evaluate_style.main(in_file, out_file, style_name)

    im = cv2.imread(out_file)
    (h, w) = im.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 90, 1.0)
    im = cv2.warpAffine(im, M, (w, h))
    im = cv2.resize(im, (2048,2048))
    cv2.imwrite(out_file,im)
    print("sending image")
    return send_file(out_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
