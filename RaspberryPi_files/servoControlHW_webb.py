#!/usr/bin/env python3 nu uita
from rpi_hardware_pwm import HardwarePWM 
import time
import os
import traceback # Utill pentru a afișa erori la inițializare

# --- Variabile Globale pentru Starea Servo-urilor ---
# Inițializăm obiectele PWM cu None. Vor fi create la prima utilizare.
pwm_pan = None
pwm_tilt = None
servos_initialized = False # Flag pentru a ști dacă inițializarea a avut loc

# Funcțiile de salvare/încărcare stare 
def save_state(pan, tilt, filename="servo_state.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{pan},{tilt}")
    except Exception as e:
        print(f"Eroare la salvarea stării servo: {e}")

def load_state(filename="servo_state.txt"):
    try:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content: # Verifică dacă fișierul nu e gol
                    pan_str, tilt_str = content.split(",")
                    pan = int(pan_str)
                    tilt = int(tilt_str)
                    if 0 <= pan <= 180 and 0 <= tilt <= 180:
                        print(f"Stare servo încărcată: Pan={pan}, Tilt={tilt}")
                        return pan, tilt
                    else:
                        print("Valorile din fișierul de stare sunt invalide.")
                else:
                    print("Fișierul de stare este gol.")
    except Exception as e:
        print(f"Nu s-a putut încărca starea anterioară ({e}), se folosesc valorile implicite.")
    print("Se returnează unghiurile implicite: Pan=90, Tilt=90")
    return 90, 90 # Valori implicite

# Încărcăm unghiurile dorite la pornire, dar NU inițializăm PWM încă
current_angle_pan, current_angle_tilt = load_state()
print(f"Unghiuri inițiale (la import): Pan={current_angle_pan}, Tilt={current_angle_tilt}")

# --- Funcția de Inițializare PWM  ---
def init_servos():
    global pwm_pan, pwm_tilt, servos_initialized, current_angle_pan, current_angle_tilt

    # Verifică dacă am inițializat deja
    if servos_initialized:
        return True

    print("[Servo Control] Încercare inițializare Hardware PWM...")
    try:
        # Cream obiectele PWM AICI
        pwm_pan = HardwarePWM(pwm_channel=0, hz=50, chip=0)
        pwm_tilt = HardwarePWM(pwm_channel=1, hz=50, chip=0) # Presupunem Tilt pe canalul 1

        # Pornim PWM la unghiurile încărcate/implicite
        pwm_pan.start(angle_to_duty(current_angle_pan))
        pwm_tilt.start(angle_to_duty(current_angle_tilt))

        servos_initialized = True
        print(f"[Servo Control] PWM inițializat și pornit cu succes la Pan={current_angle_pan}, Tilt={current_angle_tilt}.")
        return True
    except Exception as e:
        print(f"[Servo Control] !!! EROARE la inițializarea Hardware PWM: {e}")
        # Afișăm traceback detaliat în consolă pentru debug
        print("------------------- Traceback Eroare PWM Init --------------------")
        traceback.print_exc()
        print("------------------------------------------------------------------")
        pwm_pan = None # Resetăm în caz de eroare
        pwm_tilt = None
        servos_initialized = False
        return False # Semnalăm că inițializarea a eșuat

# --- Funcțiile Utilitare și de Mișcare ---
def angle_to_duty(angle):
    """Convertește unghiul (0-180) în duty cycle (2.5-12.5)."""
    # Asigură limitele unghiului pentru calcul
    angle = max(0, min(180, angle))
    return 2.5 + (angle / 180.0) * 10.0

def set_angle(pwm, target_angle, current_angle, step_delay=0.015): # Delay 
    """Mișcă servo-ul gradual de la unghiul curent la cel țintă."""
    if current_angle == target_angle:
        return target_angle # Nu e nevoie de mișcare

    # Asigură limitele unghiului țintă
    target_angle = max(0, min(180, target_angle))

    step = 1 if target_angle > current_angle else -1
    print(f"Mișcare graduală de la {current_angle} la {target_angle}...")
    # Mergem PÂNĂ la target_angle (inclusiv)
    for angle in range(int(current_angle), int(target_angle) + step, step):
        duty_cycle = angle_to_duty(angle)
        pwm.change_duty_cycle(duty_cycle)
        #print(f"Unghi intermediar: {angle} -> Duty cycle: {duty_cycle:.2f}") # Poate prea mult zgomot
        time.sleep(step_delay) # Pauză între pași

    # Asigură setarea finală exactă (deși bucla ar trebui să ajungă)
    # duty_cycle = angle_to_duty(target_angle)
    # pwm.change_duty_cycle(duty_cycle)
    # print(f"Unghi final atins: {target_angle} -> Duty cycle: {duty_cycle:.2f}")
    return target_angle # Returnează noul unghi curent

def move_camera(move_type, angle_web_str):
    """Funcția principală apelată de Flask pentru a mișca un servo."""
    global current_angle_pan, current_angle_tilt, pwm_pan, pwm_tilt, servos_initialized

    #Inițializează servo dacă nu s-a făcut deja ---
    if not servos_initialized:
        print("[move_camera] Servo neinițializate. Apel init_servos()...")
        if not init_servos():
            print("[move_camera] Eroare: Inițializarea servo a eșuat. Nu se poate mișca.")
            raise RuntimeError("Inițializarea servo a eșuat.") # Semnalează eroarea către Flask

    # Validare input ---
    try:
        angle = int(angle_web_str)
        if not (0 <= angle <= 180):
            print(f"[move_camera] Unghi invalid primit: {angle}. Trebuie 0-180.")
            raise ValueError("Unghi invalid! Introdu o valoare intre 0 si 180")
    except (ValueError, TypeError):
        print(f"[move_camera] Valoare unghi invalidă primită: '{angle_web_str}'.")
        raise ValueError("Te rog sa introduci un numar intre 0 si 180") # Semnalează eroarea

    # Execută mișcare
    if move_type == "pan":
        print(f"[move_camera] Comandă mișcare Pan de la {current_angle_pan} la {angle}")
        if pwm_pan: # Verifică dacă obiectul PWM există
            current_angle_pan = set_angle(pwm_pan, angle, current_angle_pan)
            save_state(current_angle_pan, current_angle_tilt) # Salvează noua stare
            print(f"[move_camera] Pan ajuns la {current_angle_pan}")
        else:
            print("[move_camera] Eroare: Obiectul pwm_pan nu este valid.")
            raise RuntimeError("Obiectul pwm_pan nu este valid.")
    elif move_type == "tilt":
        print(f"[move_camera] Comandă mișcare Tilt de la {current_angle_tilt} la {angle}")
        if pwm_tilt: # Verifică dacă obiectul PWM există
            current_angle_tilt = set_angle(pwm_tilt, angle, current_angle_tilt)
            save_state(current_angle_pan, current_angle_tilt) # Salvează noua stare
            print(f"[move_camera] Tilt ajuns la {current_angle_tilt}")
        else:
            print("[move_camera] Eroare: Obiectul pwm_tilt nu este valid.")
            raise RuntimeError("Obiectul pwm_tilt nu este valid.")
    else:
        print(f"[move_camera] Tip de mișcare invalid primit: '{move_type}'")
        raise ValueError("Tip de miscare invalid!")


def stop_servos():
    """Oprește ambele canale PWM."""
    global pwm_pan, pwm_tilt, servos_initialized
    print("[Servo Control] Oprire PWM...")
    if pwm_pan:
        try:
            pwm_pan.stop()
            print("- PWM Pan oprit.")
        except Exception as e:
            print(f"- Eroare la oprire PWM Pan: {e}")
    if pwm_tilt:
        try:
            pwm_tilt.stop()
            print("- PWM Tilt oprit.")
        except Exception as e:
            print(f"- Eroare la oprire PWM Tilt: {e}")
    servos_initialized = False