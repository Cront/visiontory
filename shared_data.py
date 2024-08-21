import threading

shared_frame = None
frame_lock = threading.Lock()

def get_shared_frame():
    with frame_lock:
        return shared_frame

def set_shared_frame(value):
    with frame_lock:
        global shared_frame
        shared_frame = value