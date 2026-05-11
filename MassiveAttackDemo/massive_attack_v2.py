from deepface import DeepFace
import cv2
import random
import time
import numpy as np
from datetime import datetime

print("Massive Attack Surveillance v2 - Iniciando...")
print("Teclas: 1=Normal 2=CCTV 3=Cyberpunk e=Effects ON/OFF ESC=Salir")
WEBCAM_ENABLED = False

CAP_WIDTH       = 1280
CAP_HEIGHT      = 720
ANALYZE_EVERY_N = 3
ANALYSIS_WIDTH  = 640

FONT   = cv2.FONT_HERSHEY_SIMPLEX
RED    = (0, 0, 255)
CYAN   = (255, 255, 0)
YELLOW = (0, 255, 255)
MAG    = (255, 0, 255)
GREEN  = (0, 255, 0)
WHITE  = (255, 255, 255)
MODES  = {1: "NORMAL", 2: "CCTV", 3: "CYBERPUNK"}

mode           = 1
effects_enabled = True
frame_index    = 0
last_faces     = []
total_detections = 0
prev_face_count  = 0
fps            = 0.0
fps_timer      = time.perf_counter()
fps_counter    = 0
last_timestamp = ""
last_timestamp_tick = -1

scanline_cache = {}
vignette_mask_cache = {}
cyberpunk_tint_cache = {}

def normalize_results(r):
    if isinstance(r, list): return r
    if isinstance(r, dict): return [r]
    return []

def get_scanline_overlay(shape, step=4):
    key = (shape[0], shape[1], step)
    if key in scanline_cache:
        return scanline_cache[key]

    overlay = np.full(shape, 255, dtype=np.uint8)
    overlay[::step, :, :] = 0
    scanline_cache[key] = overlay
    return overlay

def add_scanlines(frame, alpha=0.25):
    overlay = get_scanline_overlay(frame.shape, step=4)
    return cv2.addWeighted(frame, 1 - alpha, overlay, alpha, 0)

def get_vignette_mask(rows, cols):
    key = (rows, cols)
    if key in vignette_mask_cache:
        return vignette_mask_cache[key]

    k_x = cv2.getGaussianKernel(cols, cols * 0.6)
    k_y = cv2.getGaussianKernel(rows, rows * 0.6)
    kernel = k_y * k_x.T
    mask = (kernel / kernel.max()).astype(np.float32)
    mask = cv2.merge([mask, mask, mask])
    vignette_mask_cache[key] = mask
    return mask

def add_vignette(frame):
    rows, cols = frame.shape[:2]
    mask = get_vignette_mask(rows, cols)
    vignette = frame.astype(np.float32)
    vignette *= mask
    return vignette.astype(np.uint8)

def add_glitch(frame, frame_index):
    if frame_index % 30 != 0:
        return frame
    out = frame.copy()
    h   = frame.shape[0]
    y1  = random.randint(0, h - 40)
    y2  = y1 + random.randint(10, 40)
    shift = random.randint(-20, 20)
    strip = out[y1:y2, :].copy()
    strip = np.roll(strip, shift, axis=1)
    out[y1:y2, :] = strip
    return out

def add_timestamp(frame):
    global last_timestamp, last_timestamp_tick
    now = time.time()
    tick = int(now)
    if tick != last_timestamp_tick:
        last_timestamp_tick = tick
        last_timestamp = datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

    h, w = frame.shape[:2]
    cv2.putText(frame, last_timestamp, (w - 360, h - 20), FONT, 0.6, WHITE, 1)
    return frame

def add_rec_dot(frame, frame_index):
    if (frame_index // 15) % 2 == 0:
        h, w = frame.shape[:2]
        cv2.circle(frame, (w - 50, 35), 10, RED, -1)
        cv2.putText(frame, "REC", (w - 35, 40), FONT, 0.6, RED, 2)
    return frame

def apply_cctv_mode(frame):
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    return add_scanlines(frame, alpha=0.4)

def apply_cyberpunk_mode(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.8, 0, 255)
    frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    key = frame.shape[:2]
    if key in cyberpunk_tint_cache:
        tint = cyberpunk_tint_cache[key]
    else:
        tint = np.full(frame.shape, (20, 60, 0), dtype=np.uint8)
        cyberpunk_tint_cache[key] = tint

    return cv2.addWeighted(frame, 0.85, tint, 0.15, 0)

if not WEBCAM_ENABLED:
    print("Webcam deshabilitada en massive_attack_v2.py")
    raise SystemExit(0)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  CAP_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAP_HEIGHT)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

win_name = "Massive Attack Effect - ESC para salir"
cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame_index += 1
        fps_counter += 1

        now_perf = time.perf_counter()
        if now_perf - fps_timer >= 1.0:
            fps = fps_counter
            fps_counter = 0
            fps_timer = now_perf

        if frame_index % ANALYZE_EVERY_N == 0:
            scale_x = ANALYSIS_WIDTH / float(frame.shape[1])
            small   = cv2.resize(frame,
                                 (ANALYSIS_WIDTH, int(frame.shape[0] * scale_x)),
                                 interpolation=cv2.INTER_AREA)
            try:
                raw = DeepFace.analyze(
                    small,
                    actions=["age", "gender", "emotion"],
                    enforce_detection=False,
                    detector_backend="opencv",
                    align=False,
                    silent=True,
                )
                last_faces = normalize_results(raw)
                cur = len(last_faces)
                delta = cur - prev_face_count
                if delta > 0:
                    total_detections += delta
                prev_face_count = cur
            except Exception:
                last_faces = []
                prev_face_count = 0

        if   mode == 2: frame = apply_cctv_mode(frame)
        elif mode == 3: frame = apply_cyberpunk_mode(frame)

        if effects_enabled:
            frame = add_glitch(frame, frame_index)
            frame = add_vignette(frame)

            if mode == 1:
                frame = add_scanlines(frame, alpha=0.15)

        inv_scale = frame.shape[1] / float(ANALYSIS_WIDTH)
        for idx, face in enumerate(last_faces, start=1):
            region = face.get("region", {})
            if not region:
                continue
            x = int(region.get("x", 0) * inv_scale)
            y = int(region.get("y", 0) * inv_scale)
            w = int(region.get("w", 0) * inv_scale)
            h = int(region.get("h", 0) * inv_scale)

            age     = int(face.get("age", 0))
            gender  = str(face.get("dominant_gender",  "UNKNOWN")).upper()
            emotion = str(face.get("dominant_emotion", "UNKNOWN")).upper()

            cv2.rectangle(frame, (x, y), (x+w, y+h), RED, 3)
            cv2.putText(frame, f"AGE: {age}",         (x, y-30),   FONT, 0.8, CYAN,   2)
            cv2.putText(frame, f"SEX: {gender}",      (x, y-8),    FONT, 0.8, YELLOW, 2)
            cv2.putText(frame, f"EMOTION: {emotion}", (x, y+h+28), FONT, 0.8, MAG,    2)
            cv2.putText(frame, f"ID: MA-{idx:03d}",   (x, y+h+56), FONT, 0.7, RED,    2)
            cv2.putText(frame, "STATUS: SURVEILLED",  (x, y+h+84), FONT, 0.6, GREEN,  2)

        cv2.putText(frame, "MASSIVE ATTACK SURVEILLANCE SYSTEM",   (20, 50),  FONT, 1.0, RED,   3)
        cv2.putText(frame, f"FACES ON SCREEN: {len(last_faces)}",  (20, 85),  FONT, 0.7, WHITE, 2)
        cv2.putText(frame, f"TOTAL DETECTIONS: {total_detections}",(20, 110), FONT, 0.7, WHITE, 2)
        cv2.putText(frame, f"FPS: {int(fps)}",                     (20, 135), FONT, 0.6, WHITE, 2)
        cv2.putText(frame, f"MODE: {MODES[mode]}",                 (20, 160), FONT, 0.6, CYAN,  2)
        cv2.putText(frame, f"EFFECTS: {'ON' if effects_enabled else 'OFF'}", (20, 185), FONT, 0.6, WHITE, 2)

        frame = add_timestamp(frame)
        frame = add_rec_dot(frame, frame_index)

        cv2.imshow(win_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if   key == 27:         break
        elif key == ord("1"):   mode = 1
        elif key == ord("2"):   mode = 2
        elif key == ord("3"):   mode = 3
        elif key in (ord("e"), ord("E")):
            effects_enabled = not effects_enabled

finally:
    cap.release()
    cv2.destroyAllWindows()
    print(f"Demo finalizada. Total detecciones: {total_detections}")
