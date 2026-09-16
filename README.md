# Smart Waste Detection and Classification System

A computer vision project that detects and classifies waste into six categories
using a YOLO object detection model, with a Streamlit web interface and SQLite
storage for detection history.

## Problem Statement

Manual waste sorting is slow and error-prone. This project automates waste
classification from an uploaded image or live camera feed, helping demonstrate
how computer vision can assist recycling and waste management workflows.

## Objective

Build a lightweight, laptop-friendly waste detection system that:
- Accepts an image (upload or camera)
- Detects and classifies the waste item
- Displays the predicted class and confidence
- Logs every detection to a local database
- Shows detection history and basic statistics

## Features

- Image upload and live camera input
- Real-time YOLO-based waste detection
- Single highest-confidence prediction per image (no duplicate/conflicting results)
- Detection history with delete support
- Statistics dashboard (totals, per-category counts, distribution, trend over time)

## Tech Stack

- Python
- Streamlit (frontend)
- Ultralytics YOLO (detection model)
- OpenCV / PIL (image handling)
- SQLite (storage)
- pandas, matplotlib (statistics)

## Dataset

**Garbage Classification** dataset (Kaggle / Roboflow, YOLO object-detection format).

- Classes (6): Biodegradable, Cardboard, Glass, Metal, Paper, Plastic
- Total images: 10,464 (7,324 train / 2,098 validation / 1,042 test)
- License: CC BY 4.0 — original dataset via Roboflow
  (`material-identification/garbage-classification-3`)

**Known limitation:** the dataset is heavily imbalanced — Biodegradable, Glass,
and Metal are well represented, while Paper and Plastic have far fewer samples.
This affects prediction accuracy for those two classes; see Model section.

## Model

- Architecture: YOLO11n (nano) — chosen for CPU/laptop-friendly training
- Trained for 10 epochs on an NVIDIA RTX 3050 (6GB)
- Model file:
- Architecture: YOLO11n (nano) — chosen for CPU/laptop-friendly training
- Trained for 10 epochs on an NVIDIA RTX 3050 (6GB)
- Model file: `training/model/best.pt` (also mirrored at `detection/models/best.pt`)

**Validation results (10 epochs):**
- Overall mAP50: ~0.348
- Plastic mAP50: ~0.145
- Paper mAP50: ~0.027

Accuracy is strongest on the well-represented classes (Biodegradable, Glass,
Metal) and weaker on Paper and Plastic due to class imbalance in the training
data — a known, documented limitation rather than a bug.

## Architecture / Workflow

## Project Structure

## Installation

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Running the App

```bash
streamlit run app.py
```

Open the sidebar and navigate between Dashboard, Upload Image, Detection
History, Statistics, and About.

## Testing

Manually verified:
- Streamlit starts without errors
- Image upload → detection → result display works
- Predictions saved to SQLite and shown correctly in Detection History
- Statistics page reflects saved detections accurately
- Sidebar navigation works across all pages

## Team

| Member | Responsibility |
|---|---|
| Shine Mathew | Dataset collection |
| Nikhil Bose | Model training (original attempt; final training redone on GPU) |
| Arjun Anish | Detection module (`detect.py`) |
| Abhidev Dileep | Streamlit frontend, SQLite database, model integration, testing, documentation |

## Future Improvements

- Rebalance or augment the dataset to improve Paper/Plastic accuracy
- Train for more epochs with a larger/varied dataset
- Add bounding box visualization on the uploaded image
- Deploy the app (e.g. Streamlit Cloud) for public access
- Add export/download of detection history as CSV
