import pprint
import cv2
import urllib.request
import json
from pyzbar.pyzbar import decode

api_key = "xczfbhupsomecymudc0xpp3ipyaob1"
scanned = list()

def BarcodeReader(frame):
    # Decode the barcodes in the frame
    detectedBarcodes = decode(frame)

    # If no barcodes are detected, print a message
    if not detectedBarcodes:
        pass
    else:
        # Traverse through all the detected barcodes in the frame
        for barcode in detectedBarcodes:
            # Locate the barcode position in the image
            (x, y, w, h) = barcode.rect

            # Draw a rectangle around the barcode
            cv2.rectangle(frame, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            url = f"https://api.barcodelookup.com/v3/products?barcode={barcode.data.decode('utf-8')}&key=" + api_key

            if barcode.data:
                # print the barcode data
                cv2.putText(frame, f"Data: {barcode.data.decode('utf-8')}", (70, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            5)

                cv2.putText(frame, f"Barcode Type: {barcode.type}", (140, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),
                            5)

                # try:
                #     with urllib.request.urlopen(url) as url:
                #         data = json.loads(url.read().decode())
                #
                #     if data not in scanned:
                #         scanned.append(data)
                #
                #         print("Title: ", data["products"][0]["title"], "\n")
                #         pprint.pprint(data)
                #
                # except urllib.error.HTTPError as e:
                #     print(f"HTTP error: {e.code} - {e.reason}")
                # except urllib.error.URLError as e:
                #     print(f"URL error: {e.reason}")
                # except json.JSONDecodeError as e:
                #     print(f"JSON decode error: {e}")
                # except Exception as e:
                #     print(f"An unexpected error occurred: {e}")
                # except:
                #     continue

    return frame

if __name__ == "__main__":
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        # Capture each frame from the video feed
        ret, frame = cap.read()

        if ret:
            # Pass the frame to the BarcodeReader function
            frame = BarcodeReader(frame)

            # Display the frame with the detected barcode
            cv2.imshow("Barcode Scanner", frame)

            # Press 'q' to exit the loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("Failed to capture frame. Exiting...")
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# cap = cv2.VideoCapture(1)
# cap.set(3, 640)
# cap.set(4, 480)
#
# while True:
#     success, frame = cap.read()
#     for code in decode(frame):
#         if code.data.decode('utf-8'):
#             print("Detected")
#             (x, y, w, h) = code.rect
#             print(code.data.decode('utf-8'))
#             # Draw a rectangle around the barcode
#             cv2.rectangle(frame, (x - 10, y - 10),
#                           (x + w + 10, y + h + 10),
#                           (255, 0, 0), 2)
#             print(code.data.type)
#         else:
#             pass
#
#     cv2.imshow('Barcode Scanner', frame)
#     cv2.waitKey(1)