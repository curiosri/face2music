import cv2
import numpy as np
from utils import utils
from utils.facemesh import FaceMeshModel
from src.keypoint_classifier import KeyPointClassifier


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    facemeshmodel = FaceMeshModel()
    keypoint_classifier = KeyPointClassifier()
    
    keypoint_classifier_labels = utils.load_keypointclassifier_labels('models/weights/keypoint_classifier/keypoint_classifier_label.csv')

    while True:
         # Process Key (ESC: end)
        key = cv2.waitKey(10)
        if key == 27:  # ESC
            break
        # Camera capture
        ret, image = cap.read()
        if not ret:
            break
        image, debug_image = utils.preprocess_image(image)
        results = facemeshmodel.predict(image)
        processed_landmarks, boundingbox = facemeshmodel.process_landmarks(debug_image, results)
        
        for idx, landmarks in enumerate(processed_landmarks):
            facial_emotion_id = keypoint_classifier(landmarks)
            debug_image = utils.draw_bounding_rect(True, debug_image, boundingbox[idx])
            debug_image = utils.draw_info_text(
                    debug_image,
                    boundingbox[idx],
                    keypoint_classifier_labels[facial_emotion_id])
        
        cv2.imshow('Facial Emotion Recognition', debug_image)

    cap.release()
    cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()