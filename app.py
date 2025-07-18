import cv2
import time
import tkinter as tk
from PIL import Image, ImageTk

# Load Haarcascade Classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Initialize Webcam
cap = cv2.VideoCapture(0)

# Tkinter GUI Setup
root = tk.Tk()
root.title("Face & Eye Detector with Stable Live Preview + FPS")

video_label = tk.Label(root)
video_label.pack()

fps_label = tk.Label(root, text="FPS: 0.00", font=("Arial", 14))
fps_label.pack(pady=5)

running = False

def update_frame():
    global running
    if not running:
        return

    start_time = time.time()

    ret, frame = cap.read()
    if not ret:
        return

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))

    for (x, y, w, h) in faces:
        roi_color = frame[y:y+h, x:x+w]
        roi_gray = gray[y:y+h, x:x+w]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 10, minSize=(20, 20))
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)

    fps = 1.0 / (time.time() - start_time)
    fps_label.config(text=f"FPS: {fps:.2f}")

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(10, update_frame)  # Schedule next frame (10 ms delay)

def start_detection():
    global running
    if not running:
        running = True
        update_frame()

def stop_detection():
    global running
    running = False

def on_closing():
    stop_detection()
    cap.release()
    root.destroy()

# Buttons
start_button = tk.Button(root, text="Start Detection", font=("Arial", 14), bg="green", fg="white", command=start_detection)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Detection", font=("Arial", 14), bg="red", fg="white", command=stop_detection)
stop_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", font=("Arial", 14), bg="gray", fg="white", command=on_closing)
exit_button.pack(pady=5)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
