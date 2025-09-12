import cv2
import numpy as np
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier
from django.conf import settings
from .models import Sign
import sqlite3

MODEL_PATH = os.path.join(settings.BASE_DIR, "knn_model.pkl")
MEDIA_ROOT = settings.MEDIA_ROOT

def get_student_database():
    """Get student data from Django database"""
    students = Sign.objects.all()
    student_db = {}
    for student in students:
        # Use perm_id as the key for consistency with the original code
        student_db[f"stu_{student.id:03d}"] = {
            "name": student.name,
            "roll": student.perm_id,
            "email": student.email,
            "department": student.department
        }
    return student_db

def prepare_dataset_from_django():
    """Prepare dataset from Django media files"""
    X, y = [], []
    students = Sign.objects.all()
    
    for student in students:
        if student.image:
            img_path = os.path.join(MEDIA_ROOT, str(student.image))
            if os.path.exists(img_path):
                try:
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    if img is not None:
                        img = cv2.resize(img, (100, 100)).flatten()
                        X.append(img)
                        y.append(f"stu_{student.id:03d}")
                except Exception as e:
                    print(f"Error processing image for student {student.name}: {e}")
    
    return np.array(X), np.array(y)

def train_model_from_django():
    """Train KNN model using Django database"""
    X, y = prepare_dataset_from_django()
    
    if len(X) == 0:
        print("❌ No valid images found in database")
        return False
    
    knn = KNeighborsClassifier(n_neighbors=min(3, len(X)))
    knn.fit(X, y)
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(knn, f)
    
    print("✅ Model trained and saved with Django data.")
    return True

def recognize_faces_django():
    """Face recognition function that works with Django"""
    # Check if model exists, if not train it
    if not os.path.exists(MODEL_PATH):
        if not train_model_from_django():
            return None
    
    try:
        with open(MODEL_PATH, 'rb') as f:
            knn = pickle.load(f)
    except:
        if not train_model_from_django():
            return None
        with open(MODEL_PATH, 'rb') as f:
            knn = pickle.load(f)
    
    student_db = get_student_database()
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Try to access camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ Could not access camera")
        return None
    
    recognized_students = []
    frame_count = 0
    max_frames = 100  # Limit frames for web application
    
    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100)).flatten().reshape(1, -1)
            
            try:
                pred_id = knn.predict(face)[0]
                confidence = max(knn.predict_proba(face)[0])
                
                if confidence > 0.6:  # Add confidence threshold
                    student_info = student_db.get(pred_id, {})
                    if student_info and pred_id not in [s['id'] for s in recognized_students]:
                        recognized_students.append({
                            'id': pred_id,
                            'name': student_info.get("name", "Unknown"),
                            'roll': student_info.get("roll", "N/A"),
                            'email': student_info.get("email", "N/A"),
                            'department': student_info.get("department", "N/A"),
                            'confidence': confidence
                        })
            except Exception as e:
                print(f"Prediction error: {e}")
        
        frame_count += 1
        
        # Break if we found some students
        if len(recognized_students) > 0 and frame_count > 30:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    return recognized_students