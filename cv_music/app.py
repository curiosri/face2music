import uvicorn
from fastapi import FastAPI, File
import cv2
import numpy as np
from utils import utils
from src.facemesh import FaceMeshModel
from src.keypoint_classifier import KeyPointClassifier
from PIL import Image
from io import BytesIO

app = FastAPI(description = "CV_MUSIC_API", version ="0.1.0")
facemeshmodel = FaceMeshModel()
keypoint_classifier = KeyPointClassifier()
keypoint_classifier_labels = utils.load_keypointclassifier_labels('models/weights/keypoint_classifier/keypoint_classifier_label.csv')

@app.get('/')
async def index():
    return {'application' : 'CV_MUSIC_API', "version" : "0.1.0"}

@app.post("/predict/image")
async def predict_musicfromimage(image: bytes = File(...)):
    try:
        
        image = Image.open(BytesIO(image))
        image  = np.array(image)
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
            
        return {
            "Output" : boundingbox
        }        

    except Exception as e:
        return {"Output": f"Some issue : {e}"}

if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0",port=8000)