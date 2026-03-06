import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import get_file
import os

EMOTIONS_EN = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]
EMOTIONS_TR = ["Kizgin", "Igrenme", "Korku", "Mutlu", "Uzgun", "Saskin", "Notr"]
COLORS = {
    "Kizgin": (0, 0, 255), "Igrenme": (0, 128, 0), "Korku": (128, 0, 128),
    "Mutlu": (0, 255, 0), "Uzgun": (255, 0, 0), "Saskin": (0, 255, 255),
    "Notr": (200, 200, 200)
}

MODEL_URL = "https://github.com/oarriaga/face_classification/raw/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5"
model_path = get_file("emotion_model.hdf5", MODEL_URL, cache_subdir=os.path.join(os.getcwd(), "models"))
model = load_model(model_path, compile=False)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)
frame_count = 0
cached_faces = []

print("Kamera aciliyor... Cikmak icin 'q' tusuna bas.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    if frame_count % 3 == 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(48, 48))
        cached_faces = []

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float32") / 255.0
            roi = np.expand_dims(np.expand_dims(roi, -1), 0)

            preds = model.predict(roi, verbose=0)[0]
            dominant_idx = np.argmax(preds)
            dominant_tr = EMOTIONS_TR[dominant_idx]
            score = preds[dominant_idx]

            cached_faces.append((x, y, w, h, dominant_tr, score, preds))

    for (x, y, w, h, dominant_tr, score, preds) in cached_faces:
        color = COLORS.get(dominant_tr, (255, 255, 255))
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f"{dominant_tr} ({score:.0%})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

        # Sag tarafta duygu dagilimi
        for i, (emotion_tr, val) in enumerate(zip(EMOTIONS_TR, preds)):
            bar_w = int(val * 100)
            ty = y + 18 + i * 22
            cv2.putText(frame, emotion_tr, (x + w + 8, ty),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)
            cv2.rectangle(frame, (x + w + 80, ty - 10), (x + w + 80 + bar_w, ty), color, -1)
            cv2.putText(frame, f"{val:.0%}", (x + w + 85 + bar_w, ty),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

    cv2.imshow("Duygu Analizi", frame)
    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
