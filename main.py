'''

import cv2
import easyocr
import re
from ultralytics import YOLO


# Load YOLO license plate model
model = YOLO("models/best.pt")

# Load EasyOCR
reader = easyocr.Reader(["en"], gpu=False)

# Open video
cap = cv2.VideoCapture("videos/cmf.mp4")

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

frame_count = 0
skip_frames = 5


def clean_plate(text):

    text = text.upper()

    # Keep only letters and numbers
    text = re.sub(r"[^A-Z0-9]", "", text)

    # Basic Indian plate format
    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$"

    if re.match(pattern, text):
        return text

    return ""


while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # YOLO every 5th frame
    if frame_count % skip_frames == 0:

        results = model(
            frame,
            conf=0.75,
            imgsz=1280,
            verbose=False
        )

        for result in results:

            for box in result.boxes:

                # Get bounding box
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Crop coordinates
                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame.shape[1], x2)
                y2 = min(frame.shape[0], y2)

                # -------------------------
                # GREEN BOX = YOLO DETECTION
                # -------------------------

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )

                # Crop plate
                plate = frame[y1:y2, x1:x2]

                if plate.size == 0:
                    continue

                # Enlarge plate
                plate = cv2.resize(
                    plate,
                    None,
                    fx=3,
                    fy=3,
                    interpolation=cv2.INTER_CUBIC
                )

                # OCR
                text_results = reader.readtext(
                    plate,
                    allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                )

                raw_text = ""

                for detection in text_results:

                    text = detection[1]
                    confidence = detection[2]

                    if confidence > 0.3:
                        raw_text += text

                # Validate OCR
                plate_number = clean_plate(raw_text)

                # Display OCR only if valid
                if plate_number:

                    cv2.putText(
                        frame,
                        plate_number,
                        (x1, max(y1 - 10, 30)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

                    print(
                        f"Frame {frame_count}: {plate_number}"
                    )

                else:

                    # YOLO detected plate,
                    # but OCR could not read valid number
                    cv2.putText(
                        frame,
                        "PLATE",
                        (x1, max(y1 - 10, 30)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )


    # Show video
    cv2.imshow(
        "Traffic Plate Analysis",
        frame
    )

    # Press Q to stop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

'''
'''

import cv2 
import easyocr 
import re 
from ultralytics import YOLO 
 
# Load YOLO license plate model 
model = YOLO("models/best.pt") 
 
# Load EasyOCR 
reader = easyocr.Reader(["en"], gpu=False) 
 
# Open video 
cap = cv2.VideoCapture("videos/cmf.mp4") 
 
if not cap.isOpened(): 
    print("Error: Cannot open video") 
    exit() 
 
frame_count = 0 
skip_frames = 5 
 
 
def clean_plate(text): 
    text = text.upper() 
    text = re.sub(r"[^A-Z0-9]", "", text) 
 
    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$" 
 
    if re.match(pattern, text): 
        return text 
 
    return "" 
 
 
while True: 
 
    ret, frame = cap.read() 
 
    if not ret: 
        break 
 
    frame_count += 1 
 
    # Process every 5th frame 
    if frame_count % skip_frames == 0: 
 
        results = model( 
            frame, 
            conf=0.75, 
            imgsz=1280, 
            verbose=False 
        ) 
 
        for result in results: 
 
            for box in result.boxes: 
 
                # Get bounding box 
                x1, y1, x2, y2 = map(int, box.xyxy[0]) 
 
                # Keep coordinates inside frame 
                x1 = max(0, x1) 
                y1 = max(0, y1) 
                x2 = min(frame.shape[1], x2) 
                y2 = min(frame.shape[0], y2) 
 
                # Draw YOLO bounding box 
                cv2.rectangle( 
                    frame, 
                    (x1, y1), 
                    (x2, y2), 
                    (0, 255, 0), 
                    3 
                ) 
 
                # Crop license plate 
                plate = frame[y1:y2, x1:x2] 
 
                if plate.size == 0: 
                    continue 
 
                # Enlarge plate for OCR 
                plate = cv2.resize( 
                    plate, 
                    None, 
                    fx=3, 
                    fy=3, 
                    interpolation=cv2.INTER_CUBIC 
                ) 
 
                # OCR 
                text_results = reader.readtext( 
                    plate, 
                    allowlist="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" 
                ) 
 
                raw_text = "" 
 
                for detection in text_results: 
 
                    text = detection[1] 
                    confidence = detection[2] 
 
                    if confidence > 0.30: 
                        raw_text += text 
 
                # Clean OCR result 
                plate_number = clean_plate(raw_text) 
 
                if plate_number: 
 
                    print( 
                        f"Frame {frame_count}:{plate_number}" 
                    ) 
 
                    cv2.putText( 
                        frame, 
                        plate_number, 
                        (x1, max(y1 - 10, 30)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, 
                        (0, 255, 0), 
                        2 
                    ) 
 
                else: 
 
                    cv2.putText( 
                        frame, 
                        "PLATE", 
                        (x1, max(y1 - 10, 30)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        0.7, 
                        (0, 255, 0), 
                        2 
                    ) 
 
    # Display video 
    cv2.imshow("Traffic Plate Analysis", frame) 
 
    # Press Q to exit 
    if cv2.waitKey(1) & 0xFF == ord("q"): 
        break 
 
 
cap.release() 
cv2.destroyAllWindows()   

'''
#PaddleOCR

import cv2
import re
from ultralytics import YOLO
from paddleocr import PaddleOCR

# Load YOLO license plate model
model = YOLO("models/best.pt")

# Load PaddleOCR
ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
    enable_mkldnn=False
)

# Open video
cap = cv2.VideoCapture("videos/traffic.mp4")

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

frame_count = 0
skip_frames = 5


def clean_plate(text):
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]", "", text)

    pattern = r"^[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{3,4}$"

    if re.match(pattern, text):
        return text

    return ""


while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1

    # Process every 5th frame
    if frame_count % skip_frames == 0:

        results = model(
            frame,
            conf=0.75,
            imgsz=640,
            verbose=False
        )

        for result in results:

            for box in result.boxes:

                # YOLO bounding box
                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(frame.shape[1], x2)
                y2 = min(frame.shape[0], y2)

                # Draw plate box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    3
                )

                # Crop plate
                plate = frame[y1:y2, x1:x2]

                if plate.size == 0:
                    continue

                # Resize plate
                plate = cv2.resize(
                    plate,
                    None,
                    fx=3,
                    fy=3,
                    interpolation=cv2.INTER_CUBIC
                )

                # PaddleOCR
                result_ocr = ocr.predict(plate)

                raw_text = ""

                for res in result_ocr:

                    data = res.json

                    if isinstance(data, str):
                        import json
                        data = json.loads(data)

                    data = data.get("res", data)

                    texts = data.get("rec_texts", [])

                    for text in texts:
                        raw_text += text

                # Clean OCR result
                plate_number = clean_plate(raw_text)

                if plate_number:

                    print(
                        f"Frame {frame_count}: {plate_number}"
                    )

                    cv2.putText(
                        frame,
                        plate_number,
                        (x1, max(y1 - 10, 30)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 0),
                        2
                    )

                else:

                    cv2.putText(
                        frame,
                        "PLATE",
                        (x1, max(y1 - 10, 30)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )

    # Display video
    cv2.imshow(
        "YOLO + PaddleOCR License Plate Recognition",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

