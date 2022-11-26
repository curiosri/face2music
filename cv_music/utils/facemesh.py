import mediapipe as mp
from src.keypoint_classifier import KeyPointClassifier
from utils import utils
import cv2

class FaceMeshModel(object):
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh    = self.mp_face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        ) 
    
    def predict(self, image : cv2.Mat):
        result = self.face_mesh.process(image)
        image.flags.writeable = True
        return result
    
    def process_landmarks(self, image, results):
        processed_landmarks = []
        boundingboxs = []
        if results.multi_face_landmarks is not None:
            for face_landmarks in results.multi_face_landmarks:
                # Bounding box calculation
                brect = utils.calc_bounding_rect(image, face_landmarks)
                # Landmark calculation
                landmark_list = utils.calc_landmark_list(image, face_landmarks)
                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = utils.pre_process_landmark(landmark_list)
                boundingboxs.append(brect)
                processed_landmarks.append(pre_processed_landmark_list)    
        
        return processed_landmarks, boundingboxs
    
    
    
    