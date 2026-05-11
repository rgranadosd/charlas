import sys
sys.path.insert(0, '/Users/rafagranados/Develop/charlas/MassiveAttackDemo/LivePortrait')
import cv2
from src.config.inference_config import InferenceConfig
from src.config.crop_config import CropConfig
from src.live_portrait_pipeline import LivePortraitPipeline

cfg  = InferenceConfig()
crop = CropConfig()
pipe = LivePortraitPipeline(inference_cfg=cfg, crop_cfg=crop)

for name in ["hulk", "monja"]:
    path = f"images/{name}.jpg"
    img  = cv2.imread(path)
    if img is None:
        print(f"NO se puede leer {path}")
        continue
    print(f"OK {name}.jpg cargada: {img.shape[1]}x{img.shape[0]}px")
    try:
        crop_info = pipe.cropper.crop_source_image(img, pipe.crop_cfg)
        if crop_info is None:
            print(f"FAIL {name}: NO se detecto cara")
        else:
            print(f"OK {name}: Cara detectada correctamente")
    except Exception as e:
        print(f"ERROR {name}: {e}")

