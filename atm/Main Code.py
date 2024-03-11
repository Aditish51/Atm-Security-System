import cv2
import dlib
import random
from tkinter import *
from tkinter import messagebox
import face_recognition

known_face_encodings = []
known_face_names = []

# Sample: Load a known face
known_face_image = face_recognition.load_image_file("ADT1.jpg")
known_face_encoding = face_recognition.face_encodings(known_face_image)[0]
known_face_encodings.append(known_face_encoding)
known_face_names.append("John Doe")

# Initialize face detector
detector = dlib.get_frontal_face_detector()

# Generate a random OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# Validate PIN
def validate_pin():
    entered_pin = pin_entry.get()
    if entered_pin == "1234":  # Replace with your desired PIN
        messagebox.showinfo("Success", "PIN Verified!")
        generate_otp_button.config(state=NORMAL)
    else:
        messagebox.showerror("Error", "Invalid PIN")

# Face detection function
def detect_face():
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = detector(gray)
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if the face matches any of the known faces
         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

         name = "Unknown"

         if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

# Generate OTP and show it
def generate_and_show_otp():
    generated_otp = generate_otp()
    messagebox.showinfo("OTP", f"Your OTP is: {generated_otp}")

# Create GUI
root = Tk()
root.title("ATM Security System")

# PIN Entry
Label(root, text="Enter PIN:").pack()
pin_entry = Entry(root, show="*", width=50)
pin_entry.pack()

# Validate PIN Button
validate_pin_button = Button(root, text="Validate PIN", command=validate_pin)
validate_pin_button.pack()

# Face Detection Button
face_detection_button = Button(root, text="Start Face Detection", command=detect_face)
face_detection_button.pack()

# Generate OTP Button (disabled initially)
generate_otp_button = Button(root, text="Generate OTP", command=generate_and_show_otp, state=DISABLED)
generate_otp_button.pack()

root.mainloop()
