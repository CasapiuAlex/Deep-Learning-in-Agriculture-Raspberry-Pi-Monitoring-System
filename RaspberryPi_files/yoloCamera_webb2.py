# yoloCamera_webb2.py
import cv2
from ultralytics import YOLO

# Importa instanta camerei si functia de pornire din noul modul
from camera_setup import picam2, start_camera_if_needed

# Incarcarea modelului ramane la fel
model = YOLO("detectie_ncnn_model")

def gen_frames():
    """
    Generator pentru stream-ul video. Acum foloseste camera partajata.
    """
    print("[YOLO Stream] Functia gen_frames() a fost apelata.")
    
    if picam2 is None:
        print("[YOLO Stream] Eroare: Camera nu este initializata.")
        return

    # Porneste camera doar daca nu este deja pornita
    start_camera_if_needed()

    while True:
        try:
            frame = picam2.capture_array()
            results = model(frame, verbose=False)
            annotated_frame = results[0].plot()
            ret, buffer = cv2.imencode('.jpg', annotated_frame)
            if not ret:
                continue
            
            jpeg_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg_bytes + b'\r\n')

        except Exception as e:
            print(f"[YOLO Stream] Eroare in bucla generatorului: {e}")
            break
    print("[YOLO Stream] Bucla generatorului s-a terminat.")