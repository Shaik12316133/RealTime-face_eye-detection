import cv2
import tkinter as tk
from PIL import Image, ImageTk

class FaceEyeApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Real-Time Face & Eye Detection")
        self.window.configure(bg="#0f0f0f")

        self.label = tk.Label(window, bg="#0f0f0f")
        self.label.pack(padx=20, pady=20)

        self.face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        self.eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

        self.cap = cv2.VideoCapture(0)
        self.update_frame()

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
                roi_gray = gray[y:y + h, x:x + w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(frame[y:y + h, x:x + w], (ex, ey), (ex + ew, ey + eh), (255, 0, 255), 2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.window.after(10, self.update_frame)

    def on_closing(self):
        self.cap.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceEyeApp(root)
    root.mainloop()
