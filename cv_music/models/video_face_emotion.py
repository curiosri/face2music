# thanks to https://github.com/REWTAO/Facial-emotion-recognition-using-mediapipe

import csv
import copy
import itertools

import cv2 as cv
import numpy as np
import mediapipe as mp
from weights.keypoint_classifier.keypoint_classifier import KeyPointClassifier
from utils import utils

cap_device = 0
cap_width = 1920
cap_height = 1080

use_brect = True

# Camera preparation
cap = cv.VideoCapture(cap_device)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

# Model load
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
        ) 

keypoint_classifier = KeyPointClassifier()


# Read labels
keypoint_classifier_labels = utils.load_keypointclassifier_labels('models/weights/keypoint_classifier/keypoint_classifier_label.csv')

mode = 0

while True:

    # Process Key (ESC: end)
    key = cv.waitKey(10)
    if key == 27:  # ESC
        break

    # Camera capture
    ret, image = cap.read()
    if not ret:
        break
    
    image, debug_image = utils.preprocess_image(image)
    results = face_mesh.process(image)
    image.flags.writeable = True

    if results.multi_face_landmarks is not None:
        for face_landmarks in results.multi_face_landmarks:
            # Bounding box calculation
            brect = utils.calc_bounding_rect(debug_image, face_landmarks)

            # Landmark calculation
            landmark_list = utils.calc_landmark_list(debug_image, face_landmarks)

            # Conversion to relative coordinates / normalized coordinates
            pre_processed_landmark_list = utils.pre_process_landmark(
                landmark_list)

            #emotion classification
            facial_emotion_id = keypoint_classifier(pre_processed_landmark_list)
            # Drawing part
            debug_image = utils.draw_bounding_rect(use_brect, debug_image, brect)
            debug_image = utils.draw_info_text(
                    debug_image,
                    brect,
                    keypoint_classifier_labels[facial_emotion_id])

    # Screen reflection
    cv.imshow('Facial Emotion Recognition', debug_image)

cap.release()
cv.destroyAllWindows()