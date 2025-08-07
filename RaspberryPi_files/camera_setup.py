# camera_setup.py
import time
import traceback
from picamera2 import Picamera2

print("Initializare modul camera partajata (camera_setup.py)...")

picam2 = None
try:
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(
        main={"size": (640, 640), "format": "RGB888"}
    )
    picam2.configure(config)
    print("Instanta Picamera2 a fost creata si configurata cu succes.")
except Exception as e:
    print(f"!!!!!! EROARE FATALA la initializarea Picamera2: {e}")
    traceback.print_exc()

def start_camera_if_needed():
    """O functie ajutatoare pentru a porni camera daca nu este deja pornita."""
    global picam2
    if picam2 and not picam2.started:
        print("Camera nu era pornita. Se porneste acum...")
        picam2.start()
        time.sleep(1.0)
        print("Camera a fost pornita.")

def stop_camera():
    """O functie ajutatoare pentru a opri camera daca este pornita."""
    global picam2
    if picam2 and picam2.started:
        print("Camera era pornita. Se opreste acum...")
        picam2.stop()
        print("Camera a fost oprita.")