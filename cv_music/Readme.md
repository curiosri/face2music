This Repo contains source code for computer vision backend for face2music site.


Some todos have been thinking of :
- using deepface/mediapipe lib to read image and predict : ['age', 'gender', 'race', 'emotion']
- post we run these through the music recommendation algorithm 
    - which would be matching of cosine - euclidean distance matching



# run the emotion detection script :
Below should run webcam and do the detection
```
PYTHONPATH="." python main.py
```

# run the api :

```
python -m uvicorn app:app --reload
```

# curl post request :

```
curl -F "image=@/home/eulermotors/hedwig/extras/face2music/cv_music/my_photo-1.jpg" http://127.0.0.1:8000/predict/image
```