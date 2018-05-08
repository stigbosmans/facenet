from model import InceptionResNetV1
import numpy as np
import cv2
import os
from skimage.transform import resize
from scipy.spatial import distance
img_size = (160, 160, 3)

database = [{"name": "Stig", "path": "images/stig1.PNG"}, {"name": "Stig", "path": "images/stig2.PNG"}, {"name": "Stig", "path": "images/stig3.PNG"},
            {"name": "Yaiza", "path": "images/yaiza1.PNG"}, {"name": "Yaiza", "path": "images/yaiza2.PNG"}, {"name": "Yaiza", "path": "images/yaiza3.PNG"}]


def l2_normalize(x, axis=-1, epsilon=1e-10):
    output = x / np.sqrt(np.maximum(np.sum(np.square(x), axis=axis, keepdims=True), epsilon))
    return output


def crop_to_face(image, margin=10):
    cascade = cv2.CascadeClassifier("model/haarcascade_frontalface_alt2.xml")
    faces = cascade.detectMultiScale(image,
                                     scaleFactor=1.1,
                                     minNeighbors=3)
    (x, y, w, h) = faces[0]
    cropped = image[y - margin // 2:y + h + margin // 2, x - margin // 2:x + w + margin // 2, :]
    image = resize(cropped, img_size)
    return image


def load_image(path):
    img = cv2.imread(path)
    img = crop_to_face(img)
    return img


def load_images_from_database(database):
    images = []
    for item in database:
        img = load_image(item['path'])
        images.append(img)
    return images


def get_distances(anchor, embeddings):
    distances = []
    for e in embeddings:
        distances.append(distance.euclidean(anchor, e))
    return distances


model = InceptionResNetV1(weights_path="model/facenet_keras.h5")
images = load_images_from_database(database)
anchor = load_image("yaiza3.PNG")
embeddings = l2_normalize(model.predict_on_batch(np.array(images)))
anchor_embedding = l2_normalize(model.predict_on_batch(np.array([anchor])))
print(get_distances(anchor_embedding, embeddings))
print(database[np.argmin(get_distances(anchor_embedding, embeddings))]['name'])