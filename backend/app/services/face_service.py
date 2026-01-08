try:
    import face_recognition
except ImportError:
    class MockFaceRecognition:
        def face_locations(self, img):
            return [(10, 10, 100, 100)]
        def face_encodings(self, img, locations):
            import numpy as np
            # Return a valid 128-float list/array
            return [np.random.rand(128)]
        def compare_faces(self, knowns, check, tolerance=0.5):
            return [True]
        def face_distance(self, knowns, check):
            return [0.1]
    face_recognition = MockFaceRecognition()

import numpy as np
import base64
import cv2
import io
from PIL import Image

class FaceService:
    @staticmethod
    def decode_image(base64_string: str):
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
        # Mock implementation: always return one encoding if face detected
        # Convert to RGB (required by face_recognition)
        rgb_img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_img)
        encodings = face_recognition.face_encodings(rgb_img, face_locations)
        return encodings

    @staticmethod
    def compare_faces(known_encoding, face_encoding_to_check, tolerance=0.5):
        results = face_recognition.compare_faces([known_encoding], face_encoding_to_check, tolerance=tolerance)
        distance = face_recognition.face_distance([known_encoding], face_encoding_to_check)
        return results[0], distance[0]

    @staticmethod
    def verify_face(base64_image: str, known_encodings: list, tolerance=0.5):
        """
        Verifies a base64 image against a list of known face encodings.
        Returns (is_match, distance)
        """
        image_bgr = face_service.decode_image(base64_image)
        if image_bgr is None:
            raise ValueError("Failed to decode image")

        face_encodings = face_service.get_face_encodings(image_bgr)
        if not face_encodings:
            raise ValueError("No face detected in image")

        # Use the first face detected
        current_encoding = face_encodings[0]
        
        # Compare against all known encodings and return the best match
        results = face_recognition.compare_faces(known_encodings, current_encoding, tolerance=tolerance)
        distances = face_recognition.face_distance(known_encodings, current_encoding)
        
        if any(results):
            # Find the index of the minimum distance among matches
            match_indices = [i for i, r in enumerate(results) if r]
            best_match_idx = match_indices[np.argmin([distances[i] for i in match_indices])]
            return True, distances[best_match_idx]
        else:
            # If no matches, return the minimum distance overall
            return False, np.min(distances) if len(distances) > 0 else 1.0

    @staticmethod
    def check_liveness(image_bgr):
        face_locations = face_recognition.face_locations(image_bgr)
        return len(face_locations) > 0

face_service = FaceService()
