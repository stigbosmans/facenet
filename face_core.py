import face_recognition
import face_database_repo
repo = face_database_repo.FaceRepo()
import util
import os
import json

def add_face(name, file_path):
    repo.add_face(name, file_path)

def recognize(file_path):
    return face_recognition.recognize(file_path)