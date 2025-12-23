import cv2
import mss
import numpy as np
import keyboard
import time
import win32api
import win32con
import json
import os
import sys
from ultralytics import YOLO

print("--- INICIANDO MOTOR L4D2 BOT ---")

# CARGAR CONFIGURACIÓN
CONFIG_FILE = 'settings.json'
try:
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
except Exception as e:
    print(f"Error critico leyendo {CONFIG_FILE}: {e}")
    time.sleep(5)
    exit()

# ASIGNACIÓN DE VARIABLES
MODELO = config.get('model_path', 'best.pt')
CONFIDENCIA = float(config.get('confidencia', 0.25))
TECLA_ACTIVACION = config.get('tecla_activacion', 't')
TECLA_DISPARO = config.get('tecla_disparo', 'z')
TECLA_SALIR = config.get('tecla_salir', 'q')
DIVISOR_X = float(config.get('divisor_x', 10.0))
DIVISOR_Y = float(config.get('divisor_y', 9.0))
OFFSET_CABEZA = int(config.get('offset_cabeza', -5))
PACIENCIA_MEMORIA = int(config.get('paciencia_memoria', 15))
UMBRAL_PARA_EMPUJAR = float(config.get('umbral_empujar', 0.20))
UMBRAL_COLOR_DISPARO = float(config.get('umbral_color', 0.05))
MOSTRAR_VENTANA = bool(config.get('mostrar_ventana', True))
# AQUI LEEMOS LA RESOLUCION DEL SLIDER
TAMANO_CAPTURA = int(config.get('tamano_captura', 416))

# CONFIGURACIÓN DE COLOR
ROJO_BAJO1 = np.array([0, 120, 70])
ROJO_ALTO1 = np.array([10, 255, 255])
ROJO_BAJO2 = np.array([170, 120, 70])
ROJO_ALTO2 = np.array([180, 255, 255])

try:
    print(f"Cargando modelo IA: {MODELO}...")
    print(f"Resolucion de vision: {TAMANO_CAPTURA}x{TAMANO_CAPTURA}")
    model = YOLO(MODELO)
except Exception as e:
    print(f"Error cargando modelo: {e}")
    time.sleep(5)
    exit()

# Centra la captura
monitor = {
    "top": (1080 - TAMANO_CAPTURA)//2, 
    "left": (1920 - TAMANO_CAPTURA)//2, 
    "width": TAMANO_CAPTURA, 
    "height": TAMANO_CAPTURA
}
centro_img_x = TAMANO_CAPTURA // 2
centro_img_y = TAMANO_CAPTURA // 2
sct = mss.mss()
bot_activo = False
memoria_frames = 0
ultimo_diff_x = 0
ultimo_diff_y = 0

def mover_mouse_snap(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y), 0, 0)

def click_izquierdo():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.001) 
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def click_derecho():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
    time.sleep(0.05) 
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)

def analizar_rojo_global(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, ROJO_BAJO1, ROJO_ALTO1) + cv2.inRange(hsv, ROJO_BAJO2, ROJO_ALTO2)
    total = frame.shape[0] * frame.shape[1]
    return cv2.countNonZero(mask) / total if total > 0 else 0

print(f"BOT LISTO. Presiona '{TECLA_ACTIVACION.upper()}' para Activar.")
print(f"Para CERRAR el programa presiona '{TECLA_SALIR.upper()}'")

try:
    while True:
        if keyboard.is_pressed(TECLA_SALIR): 
            print("Cerrando programa...")
            break
        
        if keyboard.is_pressed(TECLA_ACTIVACION):
            bot_activo = not bot_activo
            print(f"Estado: {'[CAZANDO]' if bot_activo else '[PAUSA]'}")
            time.sleep(0.3)

        img = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        if MOSTRAR_VENTANA:
            cv2.drawMarker(frame, (centro_img_x, centro_img_y), (255, 0, 0), cv2.MARKER_CROSS, 10, 1)

        if bot_activo and keyboard.is_pressed(TECLA_DISPARO):
            # 1. DEADSTOP
            if analizar_rojo_global(frame) > UMBRAL_PARA_EMPUJAR:
                print("DEADSTOP EJECUTADO")
                click_derecho()
                time.sleep(0.15)
                continue

            # 2. AIMBOT
            results = model(frame, stream=True, verbose=False, conf=CONFIDENCIA, imgsz=TAMANO_CAPTURA)
            detectado_real = False

            for r in results:
                boxes = r.boxes
                if len(boxes) > 0:
                    box = boxes[0]
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    roi = frame[y1:y2, x1:x2]
                    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                    mask_roi = cv2.inRange(hsv_roi, ROJO_BAJO1, ROJO_ALTO1) + cv2.inRange(hsv_roi, ROJO_BAJO2, ROJO_ALTO2)
                    
                    if roi.size > 0 and (cv2.countNonZero(mask_roi) / roi.size) > UMBRAL_COLOR_DISPARO:
                        detectado_real = True
                        memoria_frames = PACIENCIA_MEMORIA 
                        
                        target_y = int(y1 + ((y2 - y1) * 0.2)) + OFFSET_CABEZA
                        target_x = int((x1 + x2) / 2)
                        
                        if MOSTRAR_VENTANA:
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                            cv2.line(frame, (centro_img_x, centro_img_y), (target_x, target_y), (0, 0, 255), 1)

                        diff_x = target_x - centro_img_x
                        diff_y = target_y - centro_img_y
                        ultimo_diff_x, ultimo_diff_y = diff_x, diff_y

                        mover_mouse_snap(diff_x / DIVISOR_X, diff_y / DIVISOR_Y)
                        if abs(diff_x) < 60 and abs(diff_y) < 60: click_izquierdo()
                        break 
            
            # 3. MEMORIA
            if not detectado_real and memoria_frames > 0:
                if MOSTRAR_VENTANA:
                    tx, ty = centro_img_x + int(ultimo_diff_x), centro_img_y + int(ultimo_diff_y)
                    cv2.line(frame, (centro_img_x, centro_img_y), (tx, ty), (0, 255, 255), 1)
                
                mover_mouse_snap(ultimo_diff_x / (DIVISOR_X * 1.2), ultimo_diff_y / (DIVISOR_Y * 1.2))
                if abs(ultimo_diff_x) < 60: click_izquierdo()
                memoria_frames -= 1

        if MOSTRAR_VENTANA:
            cv2.imshow('L4D2 AI Aimbot', frame)
            cv2.waitKey(1)

except KeyboardInterrupt: pass

cv2.destroyAllWindows()
