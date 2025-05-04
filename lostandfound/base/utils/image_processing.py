import cv2
import cv2.data
import numpy as np
import pickle
from PIL import Image as PILImage

#load Haar for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def process_image(pil_image):
    np_img = np.array(pil_image.convert("RGB"))
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)

    # face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    face_crop = None
    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_crop = gray[y:y+h, x:x+w]

    # ORB Feature detection
    orb = cv2.ORB_create()
    keypoints, descriptors = orb.detectAndCompute(gray, None)
    descriptor_data = pickle.dumps(descriptors) if descriptors is not None else None

    #face encoding is just the cropped image
    face_data = pickle.dumps(face_crop) if face_crop is not None else None

    return face_data, descriptor_data