from pyzbar.pyzbar import decode
import pprint
import cv2
import urllib.request
import json
import shared_data

print("In barcode file.")

api_key = "xczfbhupsomecymudc0xpp3ipyaob1"
scanned = list()

def barcodeReader(frame):
    print("In barcode method!")
    #barcode_found = False

    while True:

        if shared_data.shared_frame is None:
            print(f"shared_data.shared_frame is = {shared_data.shared_frame}")
            continue

        frame = shared_data.get_shared_frame().copy()

        print(f"Just set the frame equal to {frame}")

        # Decode the barcodes in the frame
        detectedBarcodes = decode(frame)

        # If no barcodes are detected, print a message
        if not detectedBarcodes:
            continue#, barcode_found

        #barcode_found = True
        # Traverse through all the detected barcodes in the frame
        for barcode in detectedBarcodes:
            # Locate the barcode position in the image
            (x, y, w, h) = barcode.rect

            # Draw a rectangle around the barcode
            cv2.rectangle(frame, (x - 10, y - 10),
                          (x + w + 10, y + h + 10),
                          (255, 0, 0), 2)

            #url = f"https://api.barcodelookup.com/v3/products?barcode={barcode.data.decode('utf-8')}&key=" + api_key

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

            # Update the shared frame
            shared_data.set_shared_frame(frame)

    #return frame#, barcode_found


def main():
    # Initialize the webcam
    cap = cv2.VideoCapture(1)
    cap.set(3, 640)
    cap.set(4, 480)

    while True:
        # Capture each frame from the video feed
        ret, frame = cap.read()

        if not ret:
            break

        # First, perform barcode detection
        #frame, barcode_detected =
        barcodeReader(frame)

        # Display the frame with the detected barcode and objects
        cv2.imshow("Camera Feed", frame)

        # Press 'q' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()