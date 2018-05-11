from flask import Flask, request
import face_core
import util
import os
import json
app = Flask(__name__)


@app.route("/face/<name>", methods=['POST'])
def face(name):
    file_path = "temp/" + util.get_random_hash() + '.jpg'
    request.files['face'].save(file_path)
    face_core.add_face(name, file_path)
    os.remove(file_path)
    return "done"


@app.route("/recognize", methods=['POST'])
def recognize():
    file_path = "temp/" + util.get_random_hash() + '.jpg'
    request.files['face'].save(file_path)
    name, score = face_core.recognize('temp/0D89AA78B5F8741C.jpg')
    os.remove(file_path)
    return json.dumps({"name": name, "score": score})


if __name__ == "__main__":
    app.run(threaded=False)