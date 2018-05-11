from model.model import InceptionResNetV1
import numpy as np
import cv2
from face_database_repo import FaceRepo
from skimage.transform import resize
from scipy.spatial import distance
img_size = (160, 160, 3)

facenet = InceptionResNetV1(weights_path="model/facenet_keras.h5")

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


def load_images(image_paths):
    images = []
    for path in image_paths:
        img = load_image(path)
        images.append(img)
    return images


def get_distances(anchor, embeddings):
    distances = []
    for e in embeddings:
        distances.append(distance.euclidean(anchor, e))
    return distances


def recognize(face_path):
    repo = FaceRepo()
    faces, labels = repo.get_all_faces()
    db_images = load_images(faces)
    anchor = load_image(face_path)
    embeddings = l2_normalize(facenet.predict_on_batch(np.array(db_images)))
    anchor_embedding = l2_normalize(facenet.predict_on_batch(np.array([anchor])))
    distances = get_distances(anchor_embedding, embeddings)
    min_index = np.argmin(distances)
    return labels[min_index], distances[min_index]

if __name__ == "__main__":
    print(f"Welcome {recognize('1525940315273.jpg')}")
    print(f"Welcome {recognize('1525940328641.jpg')}")