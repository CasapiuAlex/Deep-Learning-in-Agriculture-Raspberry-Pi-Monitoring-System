# classification_logic2.py
import numpy as np
import cv2
import time
from tensorflow import keras

# Importa instanta camerei si functia de pornire
from camera_setup import picam2, start_camera_if_needed

# Incarcarea modelului ramane la fel
MODEL_FILE = 'clasificare_CNN.keras'
class_names = ['healthy', 'powdery', 'rust']
model = keras.models.load_model(MODEL_FILE)

def preprocess_image(frame):
    img = cv2.resize(frame, (256, 256))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    return img

def perform_classification():
    """
    MODIFICAT: Nu mai primeste 'frame' ca argument.
    Captureaza, clasifica si returneaza (rezultat_text, cadru_capturat).
    """
    if picam2 is None or model is None:
        return "Eroare: Camera sau modelul nu sunt initializate.", None

    try:
        start_camera_if_needed()
        frame = picam2.capture_array()

        processed_image = preprocess_image(frame)
        predictions = model.predict(processed_image)
        
        predicted_index = np.argmax(predictions[0])
        probability = np.max(predictions[0])
        class_label = class_names[predicted_index]
        result_text = f'Predictie: {class_label} ({probability*100:.1f}%)'
        
        return result_text, frame # Returneaza si textul si imaginea

    except Exception as e:
        print(f"!!!!!! EROARE in perform_classification: {e}")
        return "A aparut o eroare in timpul clasificarii.", None