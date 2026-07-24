import random

def classify_waste(image_name):
    """
    Temporary fake AI classifier that mimics YOLO-style multi-detection.
    Returns a LIST of (waste_type, confidence) tuples —
    one for each "item" it pretends to find in the image.
    """
    
    print("RUNNING THE NEW MULTI-DETECTION VERSION")

    categories = ["Plastic", "Paper", "Metal", "Glass", "Cardboard", "Trash"]

    # Pretend the image contains somewhere between 1 and 3 different items
    num_items = random.randint(1, 3)

    # Randomly pick that many DIFFERENT categories (no repeats)
    chosen_categories = random.sample(categories, num_items)

    detections = []
    for category in chosen_categories:
        confidence = round(random.uniform(70, 99), 1)
        detections.append((category, confidence))

    return detections