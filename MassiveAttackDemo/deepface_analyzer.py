from deepface import DeepFace
import cv2
import time
import json

ANALYSIS_WIDTH = 640
OUT_FILE = "/tmp/ma_emotion.json"
WEBCAM_ENABLED = False

if not WEBCAM_ENABLED:
    print("Webcam deshabilitada en deepface_analyzer.py")
    raise SystemExit(0)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("DeepFace analyzer (multi-face) corriendo... Ctrl+C para parar")
frame_index = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue
    frame_index += 1
    if frame_index % 3 != 0:
        continue

    scale_x = ANALYSIS_WIDTH / float(frame.shape[1])
    small = cv2.resize(frame, (ANALYSIS_WIDTH, int(frame.shape[0] * scale_x)))
    inv_scale = 1.0 / scale_x

    try:
        raw = DeepFace.analyze(small, actions=["emotion", "age"],
                               enforce_detection=False,
                               detector_backend="opencv",
                               align=False, silent=True)
        faces_raw = raw if isinstance(raw, list) else [raw]

        faces_out = []
        for idx, face in enumerate(faces_raw):
            region  = face.get("region", {})
            w = int(region.get("w", 0) * inv_scale)
            h = int(region.get("h", 0) * inv_scale)
            # Ignorar detecciones triviales (sin bbox real)
            if w < 20 or h < 20:
                continue
            x1 = int(region.get("x", 0) * inv_scale)
            y1 = int(region.get("y", 0) * inv_scale)
            faces_out.append({
                "face_id": idx + 1,
                "emotion": face.get("dominant_emotion", "neutral"),
                "age":     face.get("age", "?"),
                "x1": x1,
                "y1": y1,
                "x2": x1 + w,
                "y2": y1 + h,
                "area": w * h,
            })

        # Ordenar por área descendente: la más grande = persona más prominente
        faces_out.sort(key=lambda f: f["area"], reverse=True)

        data = {"faces": faces_out, "ts": time.time()}

    except Exception:
        data = {"faces": [], "ts": time.time()}

    with open(OUT_FILE, "w") as f:
        json.dump(data, f)

cap.release()
