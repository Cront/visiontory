from barcode import barcodeReader
from cups import objectDetection
import shared_data
import cv2
import threading

print("In main file.")

def main():
    print("In main method of main file")

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    print("Webcam initialized.")

    # Start both threads for barcode and object detection
    barcodeThread = threading.Thread(target=barcodeReader())
    print("Barcode thread created.")

    objectDetectionThread = threading.Thread(target=lambda: objectDetection("cup"))
    print("Object detection thread created.")

    barcodeThread.start()
    print("Barcode thread started.")

    objectDetectionThread.start()
    print("Object detection thread started.")

    while True:
        # Capture each frame from the video feed
        ret, frame = cap.read()

        if not ret:
            print("Couldn't capture the frame.")
            break

        print("Main loop running.")

        shared_data.shared_frame = frame # Update the shared frame

        # # First, perform barcode detection
        # #frame, barcode_detected =
        # barcodeReader(frame)
        #
        # # Then, perform cup detection regardless of whether a barcode was found
        # objectDetection("cup")

        # Display the frame with the detected barcode and objects
        if shared_data.shared_frame is not None:
            print("Frame pullin' up")
            cv2.imshow("Camera Feed", shared_data.shared_frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    barcodeThread.join()
    objectDetectionThread.join()

if __name__ == "__main__":
    main()
