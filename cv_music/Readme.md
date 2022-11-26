This Repo contains source code for computer vision backend for face2music site.


Some todos have been thinking of :
- using deepface/mediapipe lib to read image and predict : ['age', 'gender', 'race', 'emotion']
- post we run these through the music recommendation algorithm 
    - which would be matching of cosine - euclidean distance matching



# run the emotion detection script :
Below should run webcam and do the detection
```
PYTHONPATH="." python models/video_face_emotion.py 
```