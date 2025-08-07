# main.py
from flask import Flask, render_template, request, jsonify, Response
import time
import atexit
import traceback
import cv2
import base64

# --- Importurile specifice din modulele noastre ---
from camera_setup import stop_camera
from yoloCamera_webb2 import gen_frames
# --- IMPORT ADUS INAPOI PENTRU SERVO ---
from servoControlHW_webb import move_camera, stop_servos 
from classification_logic2 import perform_classification

# --- INREGISTRARE FUNCTII AEXIT ADUSE INAPOI ---
atexit.register(stop_servos)
atexit.register(stop_camera)

# --- Initializare Aplicatie Flask ---
app = Flask(__name__)

# --- Variabila Globala de Stare ---
processing_mode = 'inactive'

# --- Definire Rute ---

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global processing_mode
    processing_mode = "detectie"
    return jsonify({"message": "Detectie pornita"}), 200

@app.route('/stop_processing', methods=['POST'])
def stop_processing():
    global processing_mode
    processing_mode = 'inactive'
    stop_camera()
    return jsonify({"message": "Procesare oprita"}), 200

@app.route('/video_feed')
def video_feed():
    global processing_mode
    if processing_mode == "detectie":
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return Response(status=204)

@app.route('/classify_snapshot', methods=['GET'])
def classify_snapshot():
    try:
        result_text, frame = perform_classification()
        if frame is None:
             return jsonify({"result": result_text, "image_uri": None}), 500

        ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        if not ret:
            return jsonify({"result": result_text + " (Eroare afisare imagine)", "image_uri": None}), 500

        jpeg_bytes_base64 = base64.b64encode(buffer).decode('utf-8')
        image_uri = f"data:image/jpeg;base64,{jpeg_bytes_base64}"
        
        return jsonify({"result": result_text, "image_uri": image_uri}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"result": f"Eroare server la clasificare.", "image_uri": None}), 500

# --- RUTA PENTRU SERVO ADUSA INAPOI (VERSIUNEA TA COMPLETA) ---
@app.route('/set_servo', methods=['POST'])
def set_servo():
    global move_camera
    try:
        data = request.get_json()
        if not data: return jsonify({"message": "Nu s-au primit date!"}), 400
        
        servo = data.get("servo")
        angle_str = data.get("angle")
        
        if servo not in ["pan", "tilt"]: return jsonify({"message": "Tip servo invalid!"}), 400
        
        try:
            angle = int(angle_str)
            if not (0 <= angle <= 180): raise ValueError("Unghi invalid")
        except (ValueError, TypeError): 
            return jsonify({"message": "Unghi invalid (0-180)!"}), 400
        
        try:
            move_camera(servo, str(angle))
            return jsonify({"message": f"Servo {servo} setat la {angle}°"}), 200
        except Exception as e_move:
            print(f"Eroare la move_camera: {e_move}")
            return jsonify({"message": f"Eroare neasteptata servo {servo}!"}), 500
            
    except Exception as e:
        traceback.print_exc()
        return jsonify({"message": "Eroare interna!"}), 500

# --- Pornire Server Flask ---
if __name__ == '__main__':
    print(">>> Pornire server Flask principal...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)