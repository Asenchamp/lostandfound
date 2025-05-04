import cv2
import numpy as np
import pickle
from PIL import Image as PILImage
from base.models import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def match_uploaded_image(uploaded_file):
    pil_image = PILImage.open(uploaded_file).convert("RGB")
    np_image = np.array(pil_image)
    gray = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)

    # --- Try face matching ---
    print("🧠 Searching with faces...")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        query_face = gray[y:y+h, x:x+w]

        matches = []
        for img in Image.objects.exclude(face_encoding=None):
            try:
                stored_face = pickle.loads(img.face_encoding)
                if stored_face is None:
                    continue

                query_face_resized = cv2.resize(query_face, (100, 100))
                stored_resized = cv2.resize(stored_face, (100, 100))

                hist1 = cv2.calcHist([query_face_resized], [0], None, [256], [0, 256])
                hist2 = cv2.calcHist([stored_resized], [0], None, [256], [0, 256])
                score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

                print(f"Face match score for image {img.id}: {score:.2f}")

                if score > 0.8:
                    matches.append((score, img))
            except Exception as e:
                print(f"Face match error for image {img.id}: {str(e)}")
                continue

        if matches:
            return sorted(matches, key=lambda x: -x[0])

    # --- Fallback to feature detection ---
    print("🔍 Searching with features (ORB)...")
    orb = cv2.ORB_create(nfeatures=500)
    kp1, des1 = orb.detectAndCompute(gray, None)

    if des1 is None or len(des1) < 5:
        print("No usable ORB features found.")
        return []

    matches = []
    for img in Image.objects.exclude(feature_descriptor=None):
        try:
            des2 = pickle.loads(img.feature_descriptor)
            if des2 is None or len(des2) < 5:
                continue

            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
            raw_matches = bf.match(des1, des2)
            score = len(raw_matches)

            print(f"ORB match score for image {img.id}: {score}")

            if score > 10:
                matches.append((score, img))
        except Exception as e:
            print(f"ORB match error for image {img.id}: {str(e)}")
            continue

    return sorted(matches, key=lambda x: -x[0])[:10]


















