import pytest
import numpy as np
from app.services.face_service import face_service

def test_encoding_to_bytes():
    encoding = np.random.rand(128).astype(np.float64)
    encoding_bytes = face_service.encoding_to_bytes(encoding)
    assert isinstance(encoding_bytes, bytes)
    
    # Verify we can get it back
    recovered = face_service.bytes_to_encoding(encoding_bytes)
    assert np.allclose(encoding, recovered)
    assert recovered.shape == (128,)

def test_verify_face_best_match(mocker):
    # Multiple known encodings, some match, find the best one
    known_1 = np.random.rand(128)
    known_2 = np.random.rand(128)
    current = np.random.rand(128)
    
    mocker.patch("app.services.face_service.FaceService.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.services.face_service.FaceService.get_face_encodings", return_value=[current])
    
    # Both are matches, but known_2 is closer
    mocker.patch("app.services.face_service.face_recognition.compare_faces", return_value=[True, True])
    mocker.patch("app.services.face_service.face_recognition.face_distance", return_value=[0.4, 0.2])
    
    is_match, distance = face_service.verify_face("fake_base64", [known_1, known_2])
    
    assert is_match is True
    assert distance == 0.2

def test_verify_face_no_match_returns_min_distance(mocker):
    # Multiple known encodings, none match, return min distance
    known_1 = np.random.rand(128)
    known_2 = np.random.rand(128)
    current = np.random.rand(128)
    
    mocker.patch("app.services.face_service.FaceService.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.services.face_service.FaceService.get_face_encodings", return_value=[current])
    
    mocker.patch("app.services.face_service.face_recognition.compare_faces", return_value=[False, False])
    mocker.patch("app.services.face_service.face_recognition.face_distance", return_value=[0.7, 0.6])
    
    is_match, distance = face_service.verify_face("fake_base64", [known_1, known_2])
    
    assert is_match is False
    assert distance == 0.6

def test_verify_against_encrypted_storage(mocker):
    known_1 = np.random.rand(128).astype(np.float64)
    known_1_bytes = face_service.encoding_to_bytes(known_1)
    
    # Mock decode and get_encodings
    mocker.patch("app.services.face_service.FaceService.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.services.face_service.FaceService.get_face_encodings", return_value=[known_1])
    
    # Mock DataEncryption.decrypt
    mock_decrypt = mocker.patch("app.core.encryption.DataEncryption.decrypt", return_value=known_1_bytes)
    
    # Mock face_recognition.compare_faces and face_distance
    mocker.patch("app.services.face_service.face_recognition.compare_faces", return_value=[True])
    mocker.patch("app.services.face_service.face_recognition.face_distance", return_value=[0.1])
    
    is_match, distance = face_service.verify_against_encrypted_storage("fake_base64", [b"encrypted_data"])
    
    assert is_match is True
    assert distance == 0.1
    mock_decrypt.assert_called_once_with(b"encrypted_data")
