import sys
import os
import json
import threading
sys.path.insert(0, '/Users/rafagranados/Develop/charlas/MassiveAttackDemo/LivePortrait')

import cv2
import random
import time
import numpy as np
from datetime import datetime
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline import LivePortraitPipeline
from src.utils.camera import get_rotation_matrix
from src.utils.crop import prepare_paste_back, paste_back, crop_image
from src.utils.io import load_image_rgb, resize_to_limit

print("Massive Attack Surveillance v3 - Iniciando...")
LP_PATH      = '/Users/rafagranados/Develop/charlas/MassiveAttackDemo/LivePortrait'
HULK_IMG     = os.path.join(LP_PATH, 'images/hulk.jpg')
MONJA_IMG    = os.path.join(LP_PATH, 'images/monja.jpg')
EMOTION_FILE = "/tmp/ma_emotion.json"
WEBCAM_ENABLED = False

inf_cfg  = InferenceConfig()
crop_cfg = CropConfig()
pipe     = LivePortraitPipeline(inference_cfg=inf_cfg, crop_cfg=crop_cfg)
wrapper  = pipe.live_portrait_wrapper

# ──────────────────────────────────────────────
# Pre-procesar imágenes fuente una sola vez
# ──────────────────────────────────────────────
def preprocess_source(img_path: str) -> dict:
    """Crop face, extract features – se hace UNA vez al arrancar."""
    img_rgb   = load_image_rgb(img_path)
    img_rgb   = resize_to_limit(img_rgb, inf_cfg.source_max_dim, inf_cfg.source_division)
    crop_info = pipe.cropper.crop_source_image(img_rgb, crop_cfg)
    if crop_info is None:
        raise RuntimeError(f"No face detected in {img_path}")
    img256   = crop_info['img_crop_256x256']
    I_s      = wrapper.prepare_source(img256)
    x_s_info = wrapper.get_kp_info(I_s)
    x_c_s    = x_s_info['kp']
    R_s      = get_rotation_matrix(x_s_info['pitch'], x_s_info['yaw'], x_s_info['roll'])
    f_s      = wrapper.extract_feature_3d(I_s)
    x_s      = wrapper.transform_keypoint(x_s_info)
    mask_ori = prepare_paste_back(
        inf_cfg.mask_crop, crop_info['M_c2o'],
        dsize=(img_rgb.shape[1], img_rgb.shape[0]))
    return dict(img_rgb=img_rgb, x_s_info=x_s_info,
                x_c_s=x_c_s, R_s=R_s, f_s=f_s, x_s=x_s,
                crop_info=crop_info, mask_ori=mask_ori)

print("Cargando fuentes (hulk / monja)…")
source_cache = {
    "hulk":  preprocess_source(HULK_IMG),
    "monja": preprocess_source(MONJA_IMG),
}
print("LivePortrait listo. Teclas: 1=Normal 2=CCTV 3=Cyberpunk h=Hulk m=Monja r=Reset e=Effects ESC=Salir")

# ──────────────────────────────────────────────
# Función de animación por frame (low-level)
# ──────────────────────────────────────────────
# Máscara de blending en crop-space (se crea una vez y se reutiliza)
# ──────────────────────────────────────────────
_soft_mask_crop = None

def get_soft_mask_crop():
    """Genera una versión suavizada de mask_crop para paste_back estable."""
    global _soft_mask_crop
    if _soft_mask_crop is not None:
        return _soft_mask_crop
    m = inf_cfg.mask_crop.copy()
    m_gray = cv2.cvtColor(m, cv2.COLOR_BGR2GRAY) if m.ndim == 3 else m.copy()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17))
    m_gray = cv2.erode(m_gray, kernel, iterations=2)
    m_gray = cv2.GaussianBlur(m_gray, (41, 41), 0)
    _soft_mask_crop = cv2.merge([m_gray, m_gray, m_gray]).astype(np.uint8)
    return _soft_mask_crop

# ──────────────────────────────────────────────
# Face tracking: mantener estabilidad entre frames
# ──────────────────────────────────────────────
last_face_center = None  # (cx, cy) del último face swap exitoso

def pick_closest_face(faces_from_analysis, img_bgr):
    """Usa face_analysis_wrapper para detectar caras y elegir la más cercana
    a la última posición conocida (estabilidad temporal)."""
    global last_face_center
    src_faces = pipe.cropper.face_analysis_wrapper.get(
        img_bgr,
        flag_do_landmark_2d_106=True,
        direction=crop_cfg.direction,
        max_face_num=0,  # detectar todas
    )
    if not src_faces:
        return None
    if last_face_center is None or len(src_faces) == 1:
        # Elegir la más grande (por defecto)
        best = max(src_faces, key=lambda f: (f.bbox[2]-f.bbox[0])*(f.bbox[3]-f.bbox[1]))
    else:
        # Elegir la más cercana al último centro
        lx, ly = last_face_center
        def dist(f):
            cx = (f.bbox[0] + f.bbox[2]) / 2
            cy = (f.bbox[1] + f.bbox[3]) / 2
            return (cx - lx)**2 + (cy - ly)**2
        best = min(src_faces, key=dist)
    # Actualizar centro
    last_face_center = ((best.bbox[0]+best.bbox[2])/2, (best.bbox[1]+best.bbox[3])/2)
    return best

def animate_frame_swap(webcam_bgr: np.ndarray, src: dict, ref: dict | None):
    """Face-swap: detecta cara en webcam y la reemplaza con la cara fuente animada.
    Devuelve (result_bgr, drv_info) o (None, None) si no detecta cara.
    drv_info se usa para capturar la referencia del primer frame.
    """
    frame_rgb = cv2.cvtColor(webcam_bgr, cv2.COLOR_BGR2RGB)
    img_bgr   = webcam_bgr.copy()

    # ── Detectar cara con tracking estable ──
    best_face = pick_closest_face(None, img_bgr)
    if best_face is None:
        return None, None

    lmk = best_face.landmark_2d_106
    # Re-refinar landmarks
    lmk = pipe.cropper.human_landmark_runner.run(frame_rgb, lmk)

    ret_dct = crop_image(
        frame_rgb, lmk,
        dsize=crop_cfg.dsize, scale=crop_cfg.scale,
        vx_ratio=crop_cfg.vx_ratio, vy_ratio=crop_cfg.vy_ratio,
        flag_do_rot=crop_cfg.flag_do_rot,
    )
    ret_dct["img_crop_256x256"] = cv2.resize(
        ret_dct["img_crop"], (256, 256), interpolation=cv2.INTER_AREA)

    # Extraer pose del driving (webcam)
    drv_256  = ret_dct['img_crop_256x256']
    I_d      = wrapper.prepare_source(drv_256)
    x_d_info = wrapper.get_kp_info(I_d)
    R_d      = get_rotation_matrix(x_d_info['pitch'], x_d_info['yaw'], x_d_info['roll'])

    # Info de driving para referencia
    drv_info = dict(R=R_d, exp=x_d_info['exp'].clone(),
                    scale=x_d_info['scale'], t=x_d_info['t'].clone())

    # Fuente (cacheada)
    x_s_info = src['x_s_info']
    x_c_s    = src['x_c_s']
    R_s      = src['R_s']
    f_s      = src['f_s']
    x_s      = src['x_s']

    if ref is None:
        R_new     = R_d
        delta_new = x_d_info['exp'].clone()
        scale_new = x_d_info['scale']
        t_new     = x_d_info['t'].clone()
    else:
        R_new     = (R_d @ ref['R'].permute(0, 2, 1)) @ R_s
        delta_new = x_s_info['exp'] + (x_d_info['exp'] - ref['exp'])
        scale_new = x_s_info['scale'] * (x_d_info['scale'] / ref['scale'])
        t_new     = x_s_info['t'] + (x_d_info['t'] - ref['t'])

    t_new[..., 2].fill_(0)
    x_d_new = scale_new * (x_c_s @ R_new + delta_new) + t_new
    x_d_new = wrapper.stitching(x_s, x_d_new)
    x_d_new = x_s + (x_d_new - x_s) * inf_cfg.driving_multiplier

    out = wrapper.warp_decode(f_s, x_s, x_d_new)
    I_p = wrapper.parse_output(out['out'])[0]          # 512x512 RGB uint8

    # ── Compositar con geometría estable (pipeline nativo LivePortrait) ──
    mask_ori = prepare_paste_back(
        get_soft_mask_crop(),
        ret_dct['M_c2o'],
        dsize=(frame_rgb.shape[1], frame_rgb.shape[0])
    )
    composited = paste_back(I_p, ret_dct['M_c2o'], frame_rgb, mask_ori)
    result_bgr = cv2.cvtColor(composited, cv2.COLOR_RGB2BGR)
    return result_bgr, drv_info

# ──────────────────────────────────────────────
# Thread de LivePortrait en background
# ──────────────────────────────────────────────
lp_lock      = threading.Lock()
lp_result    = None   # último BGR generado
lp_busy      = False
lp_pending   = None   # frame webcam pendiente
lp_mode      = None
lp_ref       = None   # referencia cinemática primer frame
lp_ref_set   = False
lp_last_err  = ""     # último error del worker
lp_frames_ok = 0      # frames animados con éxito
lp_frames_tried = 0   # frames intentados

LP_LOG = "/tmp/ma_lp.log"

def lp_log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LP_LOG, "a") as _f:
            _f.write(line + "\n")
    except Exception:
        pass

def lp_worker():
    global lp_result, lp_busy, lp_pending, lp_mode, lp_ref, lp_ref_set
    global lp_last_err, lp_frames_ok, lp_frames_tried
    lp_log("LP worker thread started")
    while True:
        time.sleep(0.005)
        with lp_lock:
            if not lp_busy or lp_pending is None:
                continue
            frame_to_process = lp_pending.copy()
            mode_now  = lp_mode
            ref_now   = lp_ref if lp_ref_set else None
            lp_pending = None

        if mode_now not in source_cache:
            lp_log(f"[LP WARN] mode '{mode_now}' not in source_cache")
            with lp_lock: lp_busy = False
            continue

        src = source_cache[mode_now]
        try:
            with lp_lock:
                lp_frames_tried += 1
                frame_num = lp_frames_tried
            result, drv_info = animate_frame_swap(frame_to_process, src, ref_now)
            if result is not None:
                # Capturar referencia del primer frame válido
                if ref_now is None and drv_info is not None:
                    with lp_lock:
                        lp_ref     = drv_info
                        lp_ref_set = True
                    lp_log(f"[LP] Reference frame captured for mode={mode_now}")
                with lp_lock:
                    lp_result = result
                    lp_frames_ok += 1
                    if lp_frames_ok == 1:
                        lp_log(f"[LP] First successful swap frame! mode={mode_now}")
            else:
                lp_log(f"[LP WARN] No face in webcam frame#{frame_num}")
                with lp_lock:
                    lp_last_err = "No face detected in webcam"
        except Exception as ex:
            import traceback
            tb = traceback.format_exc()
            lp_log(f"[LP ERROR] {ex}\n{tb}")
            with lp_lock:
                lp_last_err = str(ex)[:60]
        with lp_lock:
            lp_busy = False

lp_thread = threading.Thread(target=lp_worker, daemon=True)
lp_thread.start()

def request_lp(frame: np.ndarray, mode: str):
    global lp_busy, lp_pending, lp_mode
    with lp_lock:
        if not lp_busy:
            lp_busy   = True
            lp_pending = frame.copy()
            lp_mode   = mode

def reset_lp():
    global lp_result, lp_ref, lp_ref_set, lp_last_err, lp_frames_ok, lp_frames_tried
    global last_face_center
    with lp_lock:
        lp_result        = None
        lp_ref           = None
        lp_ref_set       = False
        lp_last_err      = ""
        lp_frames_ok     = 0
        lp_frames_tried  = 0
        last_face_center = None

# ──────────────────────────────────────────────
# Efectos visuales (con caché)
# ──────────────────────────────────────────────
CAP_WIDTH=1280; CAP_HEIGHT=720; ANALYZE_EVERY_N=3; TRIGGER_SECS=2.0
FONT=cv2.FONT_HERSHEY_SIMPLEX; RED=(0,0,255); CYAN=(255,255,0)
GREEN=(0,255,0); WHITE=(255,255,255); ORANGE=(0,165,255)
COLORS_FACE=[(0,255,0),(0,200,255),(255,100,0),(200,0,255),(255,255,0)]
MODES={1:"NORMAL",2:"CCTV",3:"CYBERPUNK"}

scanline_cache={}; vignette_mask_cache={}; cyberpunk_tint_cache={}

def get_scanline_overlay(shape, step=4):
    key=(shape[0],shape[1],step)
    if key not in scanline_cache:
        o=np.full(shape,255,dtype=np.uint8); o[::step,:,:]=0; scanline_cache[key]=o
    return scanline_cache[key]

def add_scanlines(frame, alpha=0.25):
    return cv2.addWeighted(frame,1-alpha,get_scanline_overlay(frame.shape),alpha,0)

def get_vignette_mask(rows, cols):
    key=(rows,cols)
    if key not in vignette_mask_cache:
        kx=cv2.getGaussianKernel(cols,cols*0.6); ky=cv2.getGaussianKernel(rows,rows*0.6)
        m=(ky*kx.T); m=(m/m.max()).astype(np.float32); vignette_mask_cache[key]=cv2.merge([m,m,m])
    return vignette_mask_cache[key]

def add_vignette(frame):
    r,c=frame.shape[:2]
    return (frame.astype(np.float32)*get_vignette_mask(r,c)).astype(np.uint8)

def add_glitch(frame,fi):
    if fi%30!=0: return frame
    out=frame.copy(); h=frame.shape[0]
    y1=random.randint(0,h-40); y2=y1+random.randint(10,40)
    out[y1:y2,:]=np.roll(out[y1:y2,:].copy(),random.randint(-20,20),axis=1)
    return out

def add_timestamp(frame):
    global last_timestamp, last_timestamp_tick
    tick=int(time.time())
    if tick!=last_timestamp_tick:
        last_timestamp_tick=tick; last_timestamp=datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
    h,w=frame.shape[:2]; cv2.putText(frame,last_timestamp,(w-360,h-20),FONT,0.6,WHITE,1)
    return frame

def add_rec_dot(frame,fi):
    if (fi//15)%2==0:
        h,w=frame.shape[:2]; cv2.circle(frame,(w-50,35),10,RED,-1)
        cv2.putText(frame,"REC",(w-35,40),FONT,0.6,RED,2)
    return frame

def apply_cctv_mode(frame):
    return add_scanlines(cv2.cvtColor(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY),cv2.COLOR_GRAY2BGR),alpha=0.4)

def apply_cyberpunk_mode(frame):
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:,:,1]=np.clip(hsv[:,:,1]*1.8,0,255)
    frame=cv2.cvtColor(hsv.astype(np.uint8),cv2.COLOR_HSV2BGR)
    key=frame.shape[:2]
    if key not in cyberpunk_tint_cache:
        cyberpunk_tint_cache[key]=np.full(frame.shape,(20,60,0),dtype=np.uint8)
    return cv2.addWeighted(frame,0.85,cyberpunk_tint_cache[key],0.15,0)

def get_face_area(face: dict) -> int:
    x1 = int(face.get("x1", 0)); y1 = int(face.get("y1", 0))
    x2 = int(face.get("x2", 0)); y2 = int(face.get("y2", 0))
    return max(0, x2 - x1) * max(0, y2 - y1)

def pick_trigger_face(faces: list[dict]) -> dict | None:
    global trigger_face_id
    if not faces:
        return None
    if trigger_face_id is not None:
        for face in faces:
            if face.get("face_id") == trigger_face_id:
                return face
    return max(faces, key=get_face_area)

def reset_trigger_state():
    global trigger_face_id, trigger_emotion, trigger_start
    trigger_face_id = None
    trigger_emotion = None
    trigger_start = 0.0

def update_emotion_trigger(emotion: str, face_id):
    global transform_mode, trigger_face_id, trigger_emotion, trigger_start
    if transform_mode is not None:
        return
    now = time.time()
    emotion = emotion.lower()
    if emotion in ("angry", "disgust"):
        if face_id != trigger_face_id or emotion != trigger_emotion:
            trigger_face_id = face_id
            trigger_emotion = emotion
            trigger_start = now
            return
        if now - trigger_start >= TRIGGER_SECS:
            new_mode = "hulk" if emotion == "angry" else "monja"
            transform_mode = new_mode
            reset_lp()
            lp_log(f"[LP] Emotion trigger: {emotion} → {new_mode}")
    else:
        reset_trigger_state()

# ──────────────────────────────────────────────
# Estado principal
# ──────────────────────────────────────────────
mode=1; effects_enabled=True; frame_index=0
fps=0.0; fps_timer=time.perf_counter(); fps_counter=0
last_timestamp=""; last_timestamp_tick=-1
transform_mode=None
trigger_face_id=None; trigger_emotion=None; trigger_start=0.0
current_emotion="neutral"; hud_faces=[]

if not WEBCAM_ENABLED:
    print("Webcam deshabilitada por configuración (WEBCAM_ENABLED=False).")
    sys.exit(0)

cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,CAP_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,CAP_HEIGHT)
cap.set(cv2.CAP_PROP_BUFFERSIZE,1)
win_name="Massive Attack Surveillance v3 - ESC para salir"
cv2.namedWindow(win_name,cv2.WINDOW_NORMAL)

try:
    while cap.isOpened():
        ret,frame=cap.read()
        if not ret: continue
        frame_index+=1; fps_counter+=1
        now_perf=time.perf_counter()
        if now_perf-fps_timer>=1.0:
            fps=fps_counter; fps_counter=0; fps_timer=now_perf

        # Leer datos de emoción (multi-cara)
        if frame_index%ANALYZE_EVERY_N==0:
            try:
                with open(EMOTION_FILE) as f:
                    hud_data=json.load(f)
                hud_faces=hud_data.get("faces",[])
                dominant_face = pick_trigger_face(hud_faces)
                if dominant_face:
                    current_emotion=dominant_face.get("emotion","neutral")
                    update_emotion_trigger(current_emotion, dominant_face.get("face_id"))
                else:
                    reset_trigger_state()
            except Exception:
                pass

        # ── LivePortrait / display frame ──
        if transform_mode in ("hulk","monja"):
            request_lp(frame, transform_mode)
            with lp_lock:
                display_frame = lp_result.copy() if lp_result is not None else frame.copy()
        else:
            with lp_lock:
                if lp_result is not None: lp_result=None
            display_frame=frame.copy()
            if mode==2: display_frame=apply_cctv_mode(display_frame)
            elif mode==3: display_frame=apply_cyberpunk_mode(display_frame)

        if effects_enabled:
            display_frame=add_glitch(display_frame,frame_index)
            display_frame=add_vignette(display_frame)
            if mode==1 and transform_mode is None:
                display_frame=add_scanlines(display_frame,alpha=0.15)

        # ── HUD principal ──
        hud_color=ORANGE if transform_mode else RED
        mode_label=transform_mode.upper() if transform_mode else MODES[mode]
        cv2.putText(display_frame,"MASSIVE ATTACK SURVEILLANCE SYSTEM",(20,50),FONT,1.0,hud_color,3)
        cv2.putText(display_frame,f"FACES: {len(hud_faces)}",(20,85),FONT,0.7,WHITE,2)
        cv2.putText(display_frame,f"FPS: {int(fps)}",(20,110),FONT,0.6,WHITE,2)
        cv2.putText(display_frame,f"MODE: {mode_label}",(20,135),FONT,0.6,CYAN,2)
        cv2.putText(display_frame,f"EFFECTS: {'ON' if effects_enabled else 'OFF'}",(20,160),FONT,0.6,WHITE,2)
        if transform_mode:
            with lp_lock:
                ok_frames = lp_frames_ok
                tried     = lp_frames_tried
                last_err  = lp_last_err
            lp_status = f"LP: {ok_frames}/{tried}"
            lp_color  = GREEN if ok_frames > 0 else (RED if tried > 0 else WHITE)
            cv2.putText(display_frame, lp_status, (20, 183), FONT, 0.55, lp_color, 2)
            if last_err:
                cv2.putText(display_frame, last_err[:45], (20, 205), FONT, 0.45, RED, 1)

        # ── Bounding boxes de TODAS las caras detectadas ──
        for i, face in enumerate(hud_faces):
            color=COLORS_FACE[i % len(COLORS_FACE)]
            x1b=face.get("x1",0); y1b=face.get("y1",0)
            x2b=face.get("x2",0); y2b=face.get("y2",0)
            if x2b>x1b and y2b>y1b:
                cv2.rectangle(display_frame,(x1b,y1b),(x2b,y2b),color,2)
                label=f"ID:{face.get('face_id',i+1)} Age:{face.get('age','?')} {face.get('emotion','?').upper()}"
                cv2.putText(display_frame,label,(x1b,max(y1b-8,14)),FONT,0.55,color,2)

        # ── Barra de trigger (cara más prominente) ──
        if transform_mode is None and hud_faces:
            dom_e=current_emotion.lower()
            if trigger_emotion == dom_e and trigger_start > 0:
                elapsed=time.time()-trigger_start
                bar_w=int(200*min(elapsed/TRIGGER_SECS,1.0))
                cv2.rectangle(display_frame,(20,175),(220,193),WHITE,1)
                cv2.rectangle(display_frame,(20,175),(20+bar_w,193),ORANGE,-1)
                cv2.putText(display_frame,f"TRIGGER {dom_e.upper()}: {elapsed:.1f}s",(20,213),FONT,0.5,ORANGE,1)

        display_frame=add_timestamp(display_frame)
        display_frame=add_rec_dot(display_frame,frame_index)
        cv2.imshow(win_name,display_frame)

        key=cv2.waitKey(1)&0xFF
        if key==27: break
        elif key==ord("1"): mode=1
        elif key==ord("2"): mode=2
        elif key==ord("3"): mode=3
        elif key in (ord("h"),ord("H")):
            transform_mode="hulk"; reset_lp(); lp_log("[LP] Manual trigger: HULK")
        elif key in (ord("n"),ord("N")):
            transform_mode="monja"; reset_lp(); lp_log("[LP] Manual trigger: MONJA")
        elif key in (ord("m"),ord("M")):
            transform_mode="monja"; reset_lp(); lp_log("[LP] Manual trigger: MONJA")
        elif key in (ord("r"),ord("R")):
            transform_mode=None; reset_trigger_state(); reset_lp(); lp_log("[LP] Reset")
        elif key in (ord("e"),ord("E")): effects_enabled=not effects_enabled

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("Demo finalizada.")