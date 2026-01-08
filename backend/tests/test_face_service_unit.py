import pytest
import numpy as np
import base64
from app.services.face_service import face_service

def test_decode_image_valid():
    # Create a small dummy white image in base64
    # 1x1 white pixel PNG
    base64_img = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    img = face_service.decode_image(base64_img)
    assert img is not None
    assert img.shape == (1, 1, 3)

def test_decode_image_with_prefix():
    base64_img = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    img = face_service.decode_image(base64_img)
    assert img is not None
    assert img.shape == (1, 1, 3)

def test_decode_image_invalid():
    img = face_service.decode_image("not_a_base64")
    assert img is None

def test_verify_face_match(mocker):
    # Mocking internal calls to avoid dependency on face_recognition for this unit test
    known_encoding = np.random.rand(128)
    image_encoding = known_encoding.copy()
    
    mocker.patch("app.services.face_service.face_service.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.services.face_service.face_service.get_face_encodings", return_value=[image_encoding])
    mocker.patch("app.services.face_service.face_recognition.compare_faces", return_value=[True])
    mocker.patch("app.services.face_service.face_recognition.face_distance", return_value=[0.1])
    
    # This method 'verify_face' does not exist yet
    is_match, distance = face_service.verify_face("fake_base64", [known_encoding])
    
    assert is_match is True
    assert distance == 0.1

def test_verify_face_no_match(mocker):
    known_encoding = np.random.rand(128)
    image_encoding = np.random.rand(128)
    
    mocker.patch("app.services.face_service.face_service.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.services.face_service.face_service.get_face_encodings", return_value=[image_encoding])
    mocker.patch("app.services.face_service.face_recognition.compare_faces", return_value=[False])
    mocker.patch("app.services.face_service.face_recognition.face_distance", return_value=[0.7])
    
    is_match, distance = face_service.verify_face("fake_base64", [known_encoding])
    
    assert is_match is False
    assert distance == 0.7

def test_verify_face_no_face_detected(mocker):
    known_encoding = np.random.rand(128)
    
    mocker.patch("app.services.face_service.face_service.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.services.face_service.face_service.get_face_encodings", return_value=[])
    
    with pytest.raises(ValueError, match="No face detected in image"):
        face_service.verify_face("fake_base64", [known_encoding])

def test_verify_face_decode_error(mocker):
    mocker.patch("app.services.face_service.face_service.decode_image", return_value=None)
    with pytest.raises(ValueError, match="Failed to decode image"):
        face_service.verify_face("fake_base64", [np.random.rand(128)])

def test_verify_face_empty_known_encodings(mocker):
    mocker.patch("app.services.face_service.face_service.decode_image", return_value=np.zeros((100, 100, 3)))
    mocker.patch("app.services.face_service.face_service.get_face_encodings", return_value=[np.random.rand(128)])
    mocker.patch("app.services.face_service.face_recognition.compare_faces", return_value=[])
    mocker.patch("app.services.face_service.face_recognition.face_distance", return_value=[])
    
    is_match, distance = face_service.verify_face("fake_base64", [])
    assert is_match is False
    assert distance == 1.0

def test_compare_faces_direct(mocker):
    # Testing the legacy compare_faces method
    known = np.random.rand(128)
    to_check = np.random.rand(128)
    mocker.patch("app.services.face_service.face_recognition.compare_faces", return_value=[True])
    mocker.patch("app.services.face_service.face_recognition.face_distance", return_value=[0.2])
    
    res, dist = face_service.compare_faces(known, to_check)
    assert res is True
    assert dist == 0.2

def test_check_liveness(mocker):
    mocker.patch("app.services.face_service.face_recognition.face_locations", return_value=[(1,2,3,4)])
    assert face_service.check_liveness(np.zeros((100,100,3))) is True
    
    mocker.patch("app.services.face_service.face_recognition.face_locations", return_value=[])
    assert face_service.check_liveness(np.zeros((100,100,3))) is False

def test_get_face_encodings(mocker):
    mocker.patch("app.services.face_service.face_recognition.face_locations", return_value=[(10, 10, 100, 100)])
    mocker.patch("app.services.face_service.face_recognition.face_encodings", return_value=[np.random.rand(128)])
    
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    encodings = face_service.get_face_encodings(img)
    assert len(encodings) == 1
