import cv2
import numpy as np
from utils import utils
from src.facemesh import FaceMeshModel
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
        
        if results.multi_face_landmarks is not None:    
            for face_landmarks in results.multi_face_landmarks:
                facemeshmodel.mp_drawing.draw_landmarks(
                        image=debug_image,
                        landmark_list=face_landmarks,
                        connections=facemeshmodel.mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=facemeshmodel.mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())
                facemeshmodel.mp_drawing.draw_landmarks(
                    image=debug_image,
                    landmark_list=face_landmarks,
                    connections=facemeshmodel.mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=facemeshmodel.mp_drawing_styles
                    .get_default_face_mesh_contours_style())
                facemeshmodel.mp_drawing.draw_landmarks(
                    image=debug_image,
                    landmark_list=face_landmarks,
                    connections=facemeshmodel.mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=facemeshmodel.mp_drawing_styles
                    .get_default_face_mesh_iris_connections_style())    
        
        cv2.imshow('Facial Emotion Recognition', debug_image)

    cap.release()
    cv2.destroyAllWindows()
        

if __name__ == "__main__":
    main()