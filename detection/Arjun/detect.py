import os
import st_caching if False else None
import streamlit as st
import numpy as np
from PIL import Image

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
WEIGHTS_PT = os.path.join(MODEL_DIR, 'best.pt')
WEIGHTS_H5 = os.path.join(MODEL_DIR, 'waste_classifier.h5')

@st.cache_resource
def load_trained_model():
    """
    Loads trained model weights once and caches them in memory.
    Supports YOLO (.pt) or Keras/MobileNetV2 (.h5).
    """
    if os.path.exists(WEIGHTS_PT):
        try:
            from ultralytics import YOLO
            return YOLO(WEIGHTS_PT), 'yolo'
        except Exception as e:
            st.error(f"Failed to load YOLO model: {e}")
            return None, None
    elif os.path.exists(WEIGHTS_H5):
        try:
            import tensorflow as tf
            return tf.keras.models.load_model(WEIGHTS_H5), 'keras'
        except Exception as e:
            st.error(f"Failed to load Keras model: {e}")
            return None, None
    return None, 'missing'

def classify_waste(image_input):
    """
    Unified prediction interface.
    Returns: waste_type (str), confidence (float)
    """
    model, model_type = load_trained_model()

    if model_type == 'missing' or model is None:
        # Graceful fallback notification while model training is in progress
        st.info("⚠️ Trained model file (models/best.pt or models/waste_classifier.h5) not found. Displaying fallback prediction.")
        return "plastic", 0.85

    if model_type == 'yolo':
        results = model(image_input)
        for r in results:
            if len(r.boxes) > 0:
                top_box = r.boxes[0]
                cls_id = int(top_box.cls[0])
                conf = float(top_box.conf[0])
                label = model.names[cls_id]
                return label, conf
        return "organic", 0.50

    elif model_type == 'keras':
        classes = ['cardboard', 'glass', 'metal', 'organic', 'paper', 'plastic']
        img = Image.fromarray(image_input) if isinstance(image_input, np.ndarray) else image_input
        img = img.resize((224, 224))
        img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
        preds = model.predict(img_array)
        top_idx = int(np.argmax(preds[0]))
        return classes[top_idx], float(preds[0][top_idx])

    return "unknown", 0.00