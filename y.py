import cv2
from ultralytics import YOLO

model = YOLO("models/best.pt")

cap = cv2.VideoCapture("videos/cmf.mp4")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    results = model(frame, conf=0.75, imgsz=1280, verbose=False)

    annotated = results[0].plot()

    cv2.imshow("License Plate Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()