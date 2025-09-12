import cv2
import numpy as np
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier
DATASET_PATH = "dataset/"
MODEL_PATH = "knn_model.pkl"
STUDENT_DB = {
    "stu_006": {"name": "dhyan", "roll": "102"},
    "stu_005": {"name": "Mayuresh", "roll": "101"},
    "stu_002": {"name": "Riya Sharma", "roll": "23CS102"},
    "stu_003": {"name": "Kabir Nair", "roll": "23CS103"},
}
def prepare_dataset():
    X, y = [], []
    for student_id in os.listdir(DATASET_PATH):
        student_folder = os.path.join(DATASET_PATH, student_id)
        for img_name in os.listdir(student_folder):
            img_path = os.path.join(student_folder, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (100, 100)).flatten()
            X.append(img)
            y.append(student_id)
    return np.array(X), np.array(y)
def train_model():
    X, y = prepare_dataset()
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X, y)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(knn, f)
    print("✅ Model trained and saved.")

def recognize_faces():
    with open(MODEL_PATH, 'rb') as f:
        knn = pickle.load(f)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100)).flatten().reshape(1, -1)
            pred_id = knn.predict(face)[0]
            name = STUDENT_DB.get(pred_id, {}).get("name", "Unknown")
            roll = STUDENT_DB.get(pred_id, {}).get("roll", "N/A")

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} | {roll}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        cv2.imshow("Face Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    os.makedirs(DATASET_PATH, exist_ok=True)
    if not os.path.exists(MODEL_PATH):
        train_model()
    recognize_faces()
