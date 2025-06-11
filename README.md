# Face Recognition Attendance System

This project implements a basic face recognition system to log entry and exit times for recognized individuals. It uses OpenCV for video capture and image processing, and the `face_recognition` library for face detection and recognition.

## Prerequisites

*   Python 3.6+
*   pip (Python package installer)

## Setup Instructions

1.  **Clone the Repository (if applicable)**
    If you have downloaded this as a set of files, skip this step. Otherwise, clone the repository:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Ensure `requirements.txt` is in the same directory.
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the System

1.  Execute the main script:
    ```bash
    python face_recognition_system.py
    ```

2.  You will see a menu in the console:
    *   **1. Enroll New Face:** Use this to add new individuals to the system.
    *   **2. Start Recognition:** Use this to start the face recognition and attendance logging.
    *   **3. Exit:** Close the application.

## How to Enroll New Faces

1.  Choose option '1' from the main menu.
2.  Enter the name of the person when prompted in the console.
3.  A webcam window will open.
    *   Look directly at the camera.
    *   Ensure good lighting and a clear view of your face.
    *   Press the 's' key to capture an image. The system will capture 5 images.
    *   A message in the console will indicate when each image is saved and when enrollment for that person is complete.
4.  The images will be stored in the `known_faces/<person_name>/` directory.

## Recognition and Logging

*   When you choose option '2', the system will load the known faces and start the webcam.
*   Detected faces will have a rectangle drawn around them.
    *   **Green rectangle:** Known person. Their name and current status ('entry' or 'exit') will be displayed.
    *   **Red rectangle:** Unknown person.
*   Entry and exit times are logged based on when a person is first seen or seen after a period of absence (or after their last logged status). A 5-minute cooldown is in place to avoid rapid re-logging; if seen within 5 minutes of an 'entry', it might be logged as 'exit', and if seen after 5 minutes of any log, the status will flip.
*   All attendance records are saved in `attendance_log.csv` in the same directory. The columns are: Name, Timestamp, Status.

## Notes and Limitations

*   **Lighting:** Face recognition accuracy is sensitive to lighting conditions. Ensure good, consistent lighting.
*   **One Face per Image:** The enrollment process assumes one clear face per captured image.
*   **Accuracy:** The `face_recognition` library is generally robust, but false positives or negatives can occur.
*   **CSV File:** The `attendance_log.csv` will be appended to if it already exists.

## Testing Guidelines

To ensure the system is working correctly, follow these testing steps:

1.  **Environment Setup Verification:**
    *   Follow the "Setup Instructions" carefully.
    *   Confirm that `pip install -r requirements.txt` completes without errors.

2.  **Enrollment Process:**
    *   Run `python face_recognition_system.py`.
    *   Select option '1' to enroll.
    *   Enroll at least two different individuals.
        *   Provide a clear name for each.
        *   Follow the on-screen instructions to capture images (press 's').
        *   **Check:** After enrollment, verify that directories are created under `known_faces/` for each person (e.g., `known_faces/John_Doe/`).
        *   **Check:** Confirm that image files (e.g., `John_Doe_1.jpg`, `John_Doe_2.jpg`, etc.) are present in these directories.

3.  **Recognition of Known Individuals:**
    *   Select option '2' to start recognition.
    *   Have an enrolled person face the camera.
        *   **Check:** A green rectangle should appear around their face.
        *   **Check:** Their name and status (initially 'entry') should be displayed.
        *   **Check:** A log entry should be printed to the console.
    *   Have the person leave the camera's view for a short while (e.g., 10-15 seconds) and then reappear.
        *   **Check:** According to the implemented logic, if seen within 5 minutes of an 'entry', their status should change to 'exit'. Verify this behavior.
    *   Have the person leave the camera's view for more than 5 minutes and then reappear.
        *   **Check:** Their status should flip (e.g., from 'exit' back to 'entry').
    *   Repeat with other enrolled individuals.

4.  **Recognition of Unknown Individuals:**
    *   Have a person who was *not* enrolled face the camera.
        *   **Check:** A red rectangle should appear around their face.
        *   **Check:** The label "Unknown" should be displayed.
        *   **Check:** No attendance log should be created for this "Unknown" person in the console or CSV.

5.  **Attendance Log Verification (`attendance_log.csv`):**
    *   After running a recognition session and pressing 'q' to quit, open the `attendance_log.csv` file.
        *   **Check:** The file should exist.
        *   **Check:** It should have the headers: `Name,Timestamp,Status`.
        *   **Check:** Verify that the names, timestamps, and entry/exit statuses recorded match your test actions and observations.
        *   **Check:** Run another recognition session. New logs should be appended to the file.

6.  **Basic Error Handling:**
    *   Try to start recognition (option '2') without having enrolled any faces first.
        *   **Check:** The system should inform you that no known faces are available and suggest enrolling first.

7.  **General Observations:**
    *   Note the system's performance (how quickly it recognizes faces).
    *   Test under different lighting conditions to understand its robustness.
```
