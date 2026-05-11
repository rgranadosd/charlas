from deepface import DeepFace
import cv2
import time

print("Massive Attack Surveillance - Iniciando...")
print("ESC para salir")
WEBCAM_ENABLED = False

if not WEBCAM_ENABLED:
    print("Webcam deshabilitada en massive_attack.py")
    raise SystemExit(0)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

ANALYZE_EVERY_N_FRAMES = 3
ANALYSIS_WIDTH = 640
OVERLAY_TITLE = "MASSIVE ATTACK SURVEILLANCE SYSTEM"

FONT = cv2.FONT_HERSHEY_SIMPLEX
RED = (0, 0, 255)
CYAN = (255, 255, 0)
YELLOW = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

total_detection_count = 0
current_face_count = 0
prev_face_count = 0
frame_index = 0
last_faces = []
last_inference_ms = 0.0


def normalize_results(results):
    if isinstance(results, list):
        return results
    if isinstance(results, dict):
        return [results]
    return []

try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            continue

        frame_index += 1
        height, width = frame.shape[:2]
        scale = ANALYSIS_WIDTH / float(width)
        analysis_height = int(height * scale)

        if frame_index % ANALYZE_EVERY_N_FRAMES == 0:
            small_frame = cv2.resize(
                frame,
                (ANALYSIS_WIDTH, analysis_height),
                interpolation=cv2.INTER_AREA,
            )

            start = time.perf_counter()
            try:
                results = DeepFace.analyze(
                    small_frame,
                    actions=['age', 'gender', 'emotion'],
                    enforce_detection=False,
                    detector_backend='opencv',
                    align=False,
                    silent=True,
                )
                last_faces = normalize_results(results)
                current_face_count = len(last_faces)
                delta = current_face_count - prev_face_count
                if delta > 0:
                    total_detection_count += delta
                prev_face_count = current_face_count
            except Exception:
                last_faces = []
                current_face_count = 0
                prev_face_count = 0
            last_inference_ms = (time.perf_counter() - start) * 1000.0

        inv_scale = 1.0 / scale

        for index, face in enumerate(last_faces, start=1):
            region = face.get('region', {})
            if not region:
                continue

            x = int(region.get('x', 0) * inv_scale)
            y = int(region.get('y', 0) * inv_scale)
            w = int(region.get('w', 0) * inv_scale)
            h = int(region.get('h', 0) * inv_scale)

            age = int(face.get('age', 0))
            gender = str(face.get('dominant_gender', 'UNKNOWN')).upper()
            emotion = str(face.get('dominant_emotion', 'UNKNOWN')).upper()

            cv2.rectangle(frame, (x, y), (x + w, y + h), RED, 3)

            cv2.putText(frame, f"AGE: {age}", (x, y - 30), FONT, 0.8, CYAN, 2)
            cv2.putText(frame, f"SEX: {gender}", (x, y - 8), FONT, 0.8, YELLOW, 2)
            cv2.putText(frame, f"EMOTION: {emotion}", (x, y + h + 28), FONT, 0.8, MAGENTA, 2)
            cv2.putText(frame, f"ID: MA-{index:03d}", (x, y + h + 56), FONT, 0.7, RED, 2)
            cv2.putText(frame, "STATUS: SURVEILLED", (x, y + h + 84), FONT, 0.6, GREEN, 2)

        cv2.putText(frame, OVERLAY_TITLE, (20, 50), FONT, 1.0, RED, 3)
        cv2.putText(frame, f"FACES ON SCREEN: {current_face_count}", (20, 85), FONT, 0.7, WHITE, 2)
        cv2.putText(frame, f"TOTAL DETECTIONS: {total_detection_count}", (20, 110), FONT, 0.7, WHITE, 2)
        cv2.putText(frame, f"INFERENCE: {last_inference_ms:.1f} ms", (20, 135), FONT, 0.6, WHITE, 2)
        cv2.putText(frame, f"SKIP: 1/{ANALYZE_EVERY_N_FRAMES}", (20, 160), FONT, 0.6, WHITE, 2)

        cv2.imshow("Massive Attack Effect - ESC para salir", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
finally:
    cap.release()
    cv2.destroyAllWindows()

print(f"Demo finalizada. Rostros analizados (acumulado): {total_detection_count}")
