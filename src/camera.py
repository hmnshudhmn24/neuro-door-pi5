"""Camera Interface Module"""
import cv2
import logging
import numpy as np

logger = logging.getLogger(__name__)

class Camera:
    """Camera interface for face capture"""
    
    def __init__(self, config):
        self.config = config
        self.camera_index = config.get('index', 0)
        self.cap = None
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self._initialize()
    
    def _initialize(self):
        """Initialize camera"""
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            logger.info(f"Camera initialized: index {self.camera_index}")
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            self.cap = None
    
    def capture_frame(self):
        """Capture a single frame"""
        if self.cap is None or not self.cap.isOpened():
            return None
        
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def detect_faces(self, frame):
        """Detect faces in frame"""
        if frame is None:
            return []
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        return [{'x': x, 'y': y, 'w': w, 'h': h} for (x, y, w, h) in faces]
    
    def is_active(self):
        """Check if camera is active"""
        return self.cap is not None and self.cap.isOpened()
    
    def release(self):
        """Release camera"""
        if self.cap:
            self.cap.release()
            logger.info("Camera released")
