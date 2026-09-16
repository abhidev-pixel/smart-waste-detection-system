import os
import streamlit as st
from PIL import Image
from ultralytics import YOLO

# Real trained model location
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'training', 'model')
WEIGHTS_PT = os.path.join(MODEL_DIR, 'best.pt')


@st.cache_resource
def load_trained_model():
    """Loads the trained YOLO model once and caches it in memory."""
    if not os.path.exists(WEIGHTS_PT):
        st.error(f"Trained model not found at: {WEIGHTS_PT}")
        return None, "missing"

    try:
        return YOLO(WEIGHTS_PT), "yolo"
    except Exception as e:
        st.error(f"Failed to load YOLO model: {e}")
        return None, "error"


def classify_waste(image_input):
    """
    Runs the real trained model and returns the single
    highest-confidence detection as (label, confidence).
    """
    model, model_type = load_trained_model()

    if model_type != "yolo" or model is None:
        return ("Unknown", 0.0)

    if hasattr(image_input, "seek"):
        image_input.seek(0)
    image = Image.open(image_input).convert("RGB")

    results = model.predict(
        source=image,
        imgsz=416,
        conf=0.25,
        verbose=False
    )

    best = None
    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = str(model.names[cls_id])
            if best is None or conf > best[1]:
                best = (label, conf)

    if best is None:
        return ("Unknown", 0.0)

    return best