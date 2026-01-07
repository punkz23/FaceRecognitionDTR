import face_recognition
import numpy as np
import base64
import cv2
import io
from PIL import Image

class FaceService:
    @staticmethod
    def decode_image(base64_string: str):
        """
        Decodes a base64 string into an OpenCV image (BGR).
        """
        if "base64," in base64_string:
            base64_string = base64_string.split("base64,")[1]
        
        try:
            img_data = base64.b64decode(base64_string)
            img = Image.open(io.BytesIO(img_data))
            return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"Error decoding image: {e}")
            return None

    @staticmethod
    def get_face_encodings(image_bgr):
        """
        Detects faces and returns a list of 128-d encodings.
        """
        # Convert to RGB (required by face_recognition)
        rgb_img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        
        # Find all face locations and encodings
        face_locations = face_recognition.face_locations(rgb_img)
        encodings = face_recognition.face_encodings(rgb_img, face_locations)
        
        return encodings

    @staticmethod
    def compare_faces(known_encoding, face_encoding_to_check, tolerance=0.5):
        """
        Compares a single face encoding against a known encoding.
        Returns (is_match, distance)
        """
        # face_recognition.compare_faces returns a list of booleans
        results = face_recognition.compare_faces([known_encoding], face_encoding_to_check, tolerance=tolerance)
        distance = face_recognition.face_distance([known_encoding], face_encoding_to_check)
        
        return results[0], distance[0]

    @staticmethod
    def check_liveness(image_bgr):
        """
        Basic liveness check using blink detection (Placeholder).
        In production, integrate a proper anti-spoofing model (e.g., MiniFASNet).
        """
        # Convert to grayscale for eye detection
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        
        # Load Haar cascade for eyes (Assuming the xml file exists or using dlib)
        # For this prototype, we'll simulate a pass if a face is detected
        face_locations = face_recognition.face_locations(image_bgr)
        return len(face_locations) > 0

face_service = FaceService()
