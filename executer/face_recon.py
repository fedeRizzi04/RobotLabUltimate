from threading import Thread
import face_recognition
import cv2
import numpy as np
#import body_controller as bc

imgs = "assets/faces/"

class FaceRecognizer(Thread):
    # Start Video Capture
    video_capture = cv2.VideoCapture(0)

    guaglions = face_recognition.load_image_file(imgs+"ilguaglions.jpg")
    guaglions_face_encoding = face_recognition.face_encodings(guaglions)[0]

    # Face loading
    filosofo = face_recognition.load_image_file(imgs+"filosofo.jpg")
    filosofo_face_encoding = face_recognition.face_encodings(filosofo)[0]

    cecco = face_recognition.load_image_file(imgs+"cecco.jpg")
    cecco_face_encoding = face_recognition.face_encodings(cecco)[0]

    binder = face_recognition.load_image_file(imgs+"lo.jpg")
    binder_face_encoding = face_recognition.face_encodings(binder)[0]

    teo = face_recognition.load_image_file(imgs+"teo.jpg")
    teo_face_encoding = face_recognition.face_encodings(teo)[0]

    # Set name for encodings
    known_face_encodings = [
        guaglions_face_encoding,
        filosofo_face_encoding,
        cecco_face_encoding,
        binder_face_encoding,
        teo_face_encoding,
    ]
    known_face_names = [
        "Ilguaglions",
        "Filosofo",
        "Cecco",
        "Binder",
        "Teo",
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        print("working")
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    if name == "Cecco":
                        print("Cecco")
                        #bc.lM.move_finger(1, 90)
                    elif name == "Teo":
                        print("Teo")
                        #bc.lM.move_finger(1, 90)
                        #bc.lM.move_finger(1, 180)
                    elif name == "Ilguaglions":
                        print("Ilguaglions")
                        #bc.lM.move_finger(1, 90)
                        #bc.lM.move_finger(1, 180)
                        #bc.lM.move_finger(1, 69)

                face_names.append(name)

        process_this_frame = not process_this_frame
'''
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        '''
    # Release handle to the webcam
video_capture.release()
#cv2.destroyAllWindows()
