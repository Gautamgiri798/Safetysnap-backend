from ultralytics import YOLO
import hashlib
import json
from typing import List, Dict, Tuple
import logging # Import the logging library

# Set up basic logging
logging.basicConfig(level=logging.INFO)

MODEL_PATH = 'yolov8n.pt'
model = YOLO(MODEL_PATH)

# For this demo, we'll map the 'person' class (id 0) to 'vest'.
PPE_CLASSES = {0: 'vest'} 

def detect_ppe(image_path: str) -> Tuple[List[Dict], str]:
    detections = []
    
    try:
        # --- ADDED ROBUSTNESS ---
        # This try/except block will catch any errors during model inference
        results = model(image_path)
        
        # Process results
        for result in results:
            # Check if the boxes attribute exists and is not None
            if result.boxes is None:
                continue
            
            for box in result.boxes:
                # Ensure all necessary attributes exist before accessing them
                if box.cls is None or box.xyxyn is None or box.conf is None:
                    continue

                label_id = int(box.cls[0])
                
                if label_id in PPE_CLASSES:
                    label = PPE_CLASSES[label_id]
                    x1, y1, x2, y2 = box.xyxyn[0].tolist()
                    confidence = float(box.conf[0])
                    
                    detections.append({
                        "label": label,
                        "confidence": round(confidence, 4),
                        "box": [round(x1, 4), round(y1, 4), round(x2, 4), round(y2, 4)]
                    })

    except Exception as e:
        # If the model fails for any reason, log the error and return empty results
        logging.error(f"AI model inference failed for {image_path}: {e}")
        # Return empty detections instead of crashing
        detections = []

    # --- Hashing logic remains the same ---
    # Sort to ensure consistent hash even if detection order changes
    detections.sort(key=lambda x: (x['label'], x['box']))
    detections_str = json.dumps(detections)
    detections_hash = hashlib.md5(detections_str.encode()).hexdigest()

    return detections, detections_hash