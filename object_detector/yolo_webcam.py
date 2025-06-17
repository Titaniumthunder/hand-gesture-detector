from ultralytics import YOLO
import cv2
from collections import defaultdict

# Load YOLOv8 model
model = YOLO("yolov8n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

# Memory to store total times each object entered view
object_memory = defaultdict(int)

# Track what objects were seen in the last frame
previous_frame_objects = set()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model.predict(source=frame, conf=0.5, verbose=False)
    boxes = results[0].boxes
    annotated_frame = results[0].plot()

    # Objects currently in the frame
    current_frame_objects = set()

    if boxes is not None and boxes.cls is not None:
        for cls_id in boxes.cls:
            class_name = model.names[int(cls_id)]
            current_frame_objects.add(class_name)

    # Detect new appearances: present now but weren't in previous frame
    new_appearances = current_frame_objects - previous_frame_objects
    for new_obj in new_appearances:
        object_memory[new_obj] += 1

    # Update previous frame memory
    previous_frame_objects = current_frame_objects

    # Show video feed
    cv2.imshow("YOLOv8 Memory Tracker", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Print memory after quitting
print("\n📦 Objects re-entered view:")
for obj, count in object_memory.items():
    print(f"- {obj}: {count} time(s)")
