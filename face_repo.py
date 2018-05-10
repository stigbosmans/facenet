import json
import os
import util


class FaceRepo:
    def __init__(self):
        self.database_path = 'database.json'
        self.load_db()

    def load_db(self):
        if os.path.isfile(self.database_path):
            f = open(self.database_path, 'r')
            self.db = json.loads(f.read())
            f.close()
        else:
            self.db = []
            f = open(self.database_path, 'w')
            f.write(json.dumps(self.db))
            f.close()


    def find_user(self, user_name):
        results = list(filter(lambda u: u['name'] == user_name, self.db))
        if len(results) > 0:
            return results[0]
        else:
            return None

    def add_face(self, name, face_image):
        name = name.lower()
        entry = self.find_user(name)
        image_path = os.path.join('images/', f'{name}_{util.get_random_hash()}.jpg')
        util.write_image(image_path, face_image)
        if entry is not None:
            entry['faces'].append(image_path)
        else:
            entry = {
                'name': name,
                'faces': [
                    image_path
                ]
            }
            self.db.append(entry)
        self.flush()

    def get_all_faces(self):
        labels = []
        faces = []
        for i in self.db:
            for f in i['faces']:
                faces.append(f)
                labels.append(i['name'])
        return faces, labels

    def flush(self):
        f = open(self.database_path, 'w')
        f.write(json.dumps(self.db))
        f.close()


if __name__ == "__main__":
    repo = FaceRepo()
    repo.add_face('yaiza', 'images/yaiza1.PNG')
    repo.add_face('yaiza', 'images/yaiza2.PNG')
    repo.add_face('yaiza', 'images/yaiza3.PNG')

    repo.add_face('stig', 'images/stig1.PNG')
    repo.add_face('stig', 'images/stig2.PNG')
    repo.add_face('stig', 'images/stig3.PNG')