import cv2
import json
from roboflow import Roboflow

# initializing Roboflow w/API key
rf = Roboflow(api_key="mYirPwsLGuPMcb9OAgLT")
project = rf.workspace().project("cuprecognition")
model = project.version("1").model

# initialize camera
cam = cv2.VideoCapture(0)

# set fps
fps = 30
frame_interval = int(1000 / fps)

frame_count = 0

while True:
    ret, frame = cam.read()
    # Check if frame is captured
    if not ret:
        break

    frame_count += 1
    # Skip every third frame to reduce workload
    if frame_count % 3 != 0:
        continue

    # Convert to format Roboflow expects
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (640, 480))

    # Predict on the frame
    result = model.predict(frame, confidence=90, overlap=50).json()

    # cup counter
    cup_counter = 0

    # prediction is a dictionary with "class", "confidence", "x", "y", "width", "height" keys
    for prediction in result['predictions']:
        x, y, width, height = prediction['x'], prediction['y'], prediction['width'], prediction['height']
        label = prediction['class']

        if label == "cup":
            cup_counter += 1

        # draw bounding box around the detected object
        cv2.rectangle(frame, (int(x - width / 2), int(y - height / 2)), (int(x + width / 2), int(y + height / 2)),
                      (0, 255, 0), 2)

        # put label near bounding box
        cv2.putText(frame, label, (int(x - width / 2), int(y - height / 2 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

    # # Display the cup count on the frame
    cv2.putText(frame, f"Number of Cups: {cup_counter}", (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 5)

    # Notify if fewer than 1 cup is detected
    if cup_counter < 1:
        cv2.putText(frame, "RESTOCK CUPS", (140, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)

    # display frame with predictions
    cv2.imshow('Camera Feed', frame)

    # exit on pressing 'q'
    if cv2.waitKey(frame_interval) & 0xFF == ord('q'):
        break

# when everything is done, release capture and close windows
cam.release()
cv2.destroyAllWindows()
