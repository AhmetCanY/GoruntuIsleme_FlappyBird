
"""
    Webcamden alınan görüntü ile burnun y koordinatına göre hareket eden flappy bird oyunu.
    
    Projeyi çalıştırdığımızda sağdan gelen boruların arasından geçerek oynanır.
    Herhangi bir boruya çarptıgımızda oyun sonlanır ve 1-2 saniye sonra proje kapanır. 
        
"""

import cv2 as cv
import mediapipe as mp

bird = cv.imread("images/bird.png")
pipe100 = cv.imread("images/pipe100.png")
pipe300ust = cv.imread("images/pipe300ust.png")
pipe200 = cv.imread("images/pipe200.png")
pipe200ust = cv.imread("images/pipe200ust.png")
pipe300 = cv.imread("images/pipe300.png")
pipe100ust = cv.imread("images/pipe100ust.png")
gameover = cv.imread("images/gameover.png")
a_sayac = 0
b_sayac = 0
c_sayac = 0
q_sayac = 0
durdur = 0

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# For webcam input
cap = cv.VideoCapture(0)
with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image_rows, image_cols, _ = image.shape

        image = image[0:1000, 0:1000]
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv.cvtColor(cv.flip(image, 1), cv.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = face_detection.process(image)

        # Draw the face detection annotations on the image.
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                # mp_drawing.draw_detection(image, detection)

                burun_y = int(detection.location_data.relative_keypoints[0].y * image_cols) - 40

                a_sayac = a_sayac + 4
                b_sayac = b_sayac + 4
                c_sayac = c_sayac + 4

                a_basla = 592 - a_sayac
                b_basla = 792 - b_sayac
                c_basla = 992 - c_sayac

                if a_sayac >= 0:
                    image[0:300, a_basla:642 - a_sayac] = pipe300ust
                    image[380:480, a_basla:642 - a_sayac] = pipe100
                    if (burun_y < 300 or burun_y > 350) and (111 >= a_basla >= 20):
                        durdur = 1

                if b_sayac > 200:
                    image[0:100, b_basla:842 - b_sayac] = pipe100ust
                    image[180:480, b_basla:842 - b_sayac] = pipe300
                    if (burun_y < 100 or burun_y > 150) and (111 >= b_basla >= 20):
                        durdur = 1

                if c_sayac > 400:
                    image[0:200, c_basla:1042 - c_sayac] = pipe200ust
                    image[280:480, c_basla:1042 - c_sayac] = pipe200
                    if (burun_y < 200 or burun_y > 250) and (111 >= c_basla >= 20):
                        durdur = 1

                image[0 + burun_y:29 + burun_y, 70:111] = bird

                if a_basla == 0:
                    a_sayac = 0
                if b_basla == 0:
                    b_sayac = 200
                if c_basla == 0:
                    c_sayac = 400

        if durdur == 1:
            image[240 - 21:240 + 21, 320 - 96:320 + 96] = gameover
            q_sayac = q_sayac + 1

        if q_sayac > 50:
            quit()

        cv.imshow('Burun ile Flappy Bird', image)

        if cv.waitKey(5) & 0xFF == 27:
            break

cap.release()
