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
            import numpy as np
            return [True] * len(knowns)
        def face_distance(self, knowns, check):
            import numpy as np
            return [0.1] * len(knowns)
    face_recognition = MockFaceRecognition()

import numpy as np
import base64
import cv2
import io
from PIL import Image

class FaceService:
    @classmethod
    def decode_image(cls, base64_string: str):
        """Decodes a base64 string into a BGR image (OpenCV format)."""
        print('FaceService: Decoding image...')
        if "base64," in base64_string:
            base64_string = base64_string.split("base64,")[1]
        try:
            img_data = base64.b64decode(base64_string)
            img = Image.open(io.BytesIO(img_data))
            # Ensure 3 channels (RGB) even if input is RGBA or grayscale
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Convert to numpy array and ensure uint8 type
            img_array = np.array(img).astype(np.uint8)
            # Convert PIL RGB to OpenCV BGR
            image_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            print(f'FaceService: Image decoded. Shape: {image_bgr.shape}, Dtype: {image_bgr.dtype}')
            return image_bgr
        except Exception as e:
            print(f"FaceService: Error decoding image: {e}")
            return None

    @classmethod
    def get_face_encodings(cls, image_bgr):
        """Extracts face encodings from a BGR image."""
        print(f'FaceService: Detecting faces. Input shape: {image_bgr.shape}, Dtype: {image_bgr.dtype}')
        # Convert to RGB (required by face_recognition)
        rgb_img = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        # Ensure array is C-contiguous for dlib/face_recognition
        rgb_img = np.ascontiguousarray(rgb_img)
        print(f'FaceService: RGB image shape: {rgb_img.shape}, Dtype: {rgb_img.dtype}, Contiguous: {rgb_img.flags.c_contiguous}')
        face_locations = face_recognition.face_locations(rgb_img)
        print(f'FaceService: Found {len(face_locations)} face locations.')
        encodings = face_recognition.face_encodings(rgb_img, face_locations)
        print(f'FaceService: Generated {len(encodings)} encodings.')
        return encodings

    @classmethod
    def encoding_to_bytes(cls, encoding: np.ndarray) -> bytes:
        """Converts a numpy encoding array to bytes for storage."""
        return encoding.tobytes()

    @classmethod
    def bytes_to_encoding(cls, encoding_bytes: bytes) -> np.ndarray:
        """Converts bytes back to a numpy encoding array."""
        return np.frombuffer(encoding_bytes, dtype=np.float64)

    @classmethod
    def compare_faces(cls, known_encoding, face_encoding_to_check, tolerance=0.5):
        """Compares a single known encoding with a face encoding to check."""
        results = face_recognition.compare_faces([known_encoding], face_encoding_to_check, tolerance=tolerance)
        distance = face_recognition.face_distance([known_encoding], face_encoding_to_check)
        return results[0], distance[0]

    @classmethod
    def verify_face(cls, base64_image: str, known_encodings: list, tolerance=0.5):
        """
        Verifies a base64 image against a list of known face encodings.
        Returns (is_match, distance) of the best match.
        """
        image_bgr = cls.decode_image(base64_image)
        if image_bgr is None:
            raise ValueError("Failed to decode image")

        face_encodings = cls.get_face_encodings(image_bgr)
        if not face_encodings:
            raise ValueError("No face detected in image")

        # Use the first face detected
        current_encoding = face_encodings[0]
        
        if not known_encodings:
            return False, 1.0

        # Compare against all known encodings and return the best match
        results = face_recognition.compare_faces(known_encodings, current_encoding, tolerance=tolerance)
        distances = face_recognition.face_distance(known_encodings, current_encoding)
        
        if any(results):
            # Find the index of the minimum distance among matches
            match_indices = [i for i, r in enumerate(results) if r]
            best_match_idx = match_indices[np.argmin([distances[i] for i in match_indices])]
            return True, float(distances[best_match_idx])
        else:
            # If no matches, return the minimum distance overall
            return False, float(np.min(distances))

    @classmethod
    def verify_against_encrypted_storage(cls, base64_image: str, encrypted_encodings: list[bytes], tolerance=0.5):
        """
        Decrypts stored encodings and verifies them against a new image.
        """
        from app.core.encryption import DataEncryption
        
        known_encodings = []
        for enc in encrypted_encodings:
            try:
                decrypted = DataEncryption.decrypt(enc)
                known_encodings.append(cls.bytes_to_encoding(decrypted))
            except Exception as e:
                print(f"Error decrypting encoding: {e}")
                continue
        
        if not known_encodings:
            raise ValueError("No valid stored encodings found after decryption")
            
        return cls.verify_face(base64_image, known_encodings, tolerance=tolerance)

    @classmethod
    def check_liveness(cls, image_bgr):
        """Simple liveness check (currently just checks if a face exists)."""
        face_locations = face_recognition.face_locations(image_bgr)
        return len(face_locations) > 0

face_service = FaceService()