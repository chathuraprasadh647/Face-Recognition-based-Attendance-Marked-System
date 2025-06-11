# This is the main file for the face recognition system.
# It will contain the code to load known faces, capture video from the webcam,
# detect faces in the video stream, and recognize known faces.

# Import necessary libraries
import face_recognition
import cv2
import numpy as np
import os
import datetime
import csv

KNOWN_FACES_DIR = "known_faces"

def enroll_face():
    """Captures and saves face images for a new person."""
    person_name = input("Enter the name of the person: ")
    person_dir = os.path.join(KNOWN_FACES_DIR, person_name)

    if not os.path.exists(KNOWN_FACES_DIR):
        os.makedirs(KNOWN_FACES_DIR)

    if not os.path.exists(person_dir):
        os.makedirs(person_dir)
        print(f"Directory created for {person_name} at {person_dir}")
    else:
        print(f"Directory for {person_name} already exists at {person_dir}.")
        # For now, we'll just add more images.

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    img_count = 0
    max_images = 5
    print(f"Preparing to capture {max_images} images for {person_name}.")
    print("Press 's' to save an image. Press 'q' to quit.")

    while img_count < max_images:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture image.")
            break

        cv2.imshow(f"Enroll Face - {person_name}", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            img_filename = os.path.join(person_dir, f"{person_name}_{img_count + 1}.jpg")
            cv2.imwrite(img_filename, frame)
            print(f"Saved {img_filename}")
            img_count += 1
        elif key == ord('q'):
            print("Quitting enrollment.")
            break

    cap.release()
    cv2.destroyAllWindows()

    if img_count == max_images:
        print(f"Successfully enrolled {person_name} with {max_images} images.")
    else:
        print(f"Enrollment for {person_name} incomplete. Captured {img_count}/{max_images} images.")

def load_known_faces(known_faces_dir):
    """Loads face encodings and names from the known_faces directory."""
    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(known_faces_dir):
        print(f"Directory {known_faces_dir} not found. Please enroll faces first.")
        return known_face_encodings, known_face_names

    for person_name in os.listdir(known_faces_dir):
        person_dir = os.path.join(known_faces_dir, person_name)
        if os.path.isdir(person_dir):
            for image_name in os.listdir(person_dir):
                image_path = os.path.join(person_dir, image_name)
                try:
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    if face_encodings:
                        known_face_encodings.append(face_encodings[0])
                        known_face_names.append(person_name)
                    else:
                        print(f"Warning: No face found in {image_path}. Skipping.")
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
    print(f"Loaded {len(known_face_encodings)} known face(s).")
    return known_face_encodings, known_face_names

def recognize_and_log(known_face_encodings, known_face_names):
    """Recognizes faces from webcam and logs entry/exit times."""
    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("Error: Could not open webcam.")
        return

    face_log = []
    last_seen_status = {} # {'name': {'timestamp': datetime, 'status': 'entry'/'exit'}}
    log_file_name = "attendance_log.csv"

    print("Starting face recognition. Press 'q' to quit.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
        face_locations_on_small_frame = face_recognition.face_locations(rgb_small_frame)
        face_encodings_on_small_frame = face_recognition.face_encodings(rgb_small_frame, face_locations_on_small_frame)

        # Process each detected face
        for (top_s, right_s, bottom_s, left_s), face_encoding in zip(face_locations_on_small_frame, face_encodings_on_small_frame):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            current_status_for_log = "unknown" # Status used for logging

            # Scale back up face locations to original frame size
            top, right, bottom, left = top_s * 4, right_s * 4, bottom_s * 4, left_s * 4

            if True in matches:
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    current_time = datetime.datetime.now()

                    # Determine status for logging (entry/exit)
                    if name not in last_seen_status or \
                       (current_time - last_seen_status[name]['timestamp']).total_seconds() > 300: # 5 min cooldown
                        if name not in last_seen_status or last_seen_status[name]['status'] == 'exit':
                            current_status_for_log = 'entry'
                        else:
                            current_status_for_log = 'exit'

                        last_seen_status[name] = {'timestamp': current_time, 'status': current_status_for_log}
                        log_entry = {'name': name, 'timestamp': current_time.strftime("%Y-%m-%d %H:%M:%S"), 'status': current_status_for_log}
                        face_log.append(log_entry)
                        print(f"{name} logged as {current_status_for_log} at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        # If within cooldown, use the last logged status for display
                        current_status_for_log = last_seen_status[name]['status']

            # Draw on the frame
            if name != "Unknown":
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2) # Green for known
                display_text = f"{name} ({current_status_for_log})"
                cv2.putText(frame, display_text, (left + 6, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)
            else:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2) # Red for unknown
                cv2.putText(frame, "Unknown", (left + 6, top - 10), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting recognition.")
            break

    video_capture.release()
    cv2.destroyAllWindows()

    # Save face_log to CSV
    if face_log:
        file_exists = os.path.isfile(log_file_name)
        with open(log_file_name, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['name', 'timestamp', 'status'])
            if not file_exists:
                writer.writeheader() # Write header only if file is new
            writer.writerows(face_log)
        print(f"Attendance log saved to {log_file_name}")
    else:
        print("No new entries to log.")


if __name__ == "__main__":
    while True:
        print("\nFace Recognition System")
        print("1. Enroll New Face")
        print("2. Start Recognition")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            enroll_face()
        elif choice == '2':
            known_encodings, known_names = load_known_faces(KNOWN_FACES_DIR)
            if not known_encodings:
                print("No known faces found. Please enroll faces first.")
            else:
                recognize_and_log(known_encodings, known_names)
        elif choice == '3':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")
