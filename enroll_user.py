#!/usr/bin/env python3
"""User Enrollment Utility"""
import sys
import cv2
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.database import Database
from src.camera import Camera
from src.face_recognition import FaceRecognitionEngine

def enroll_user():
    print("=" * 60)
    print("NeuroDoor-Pi5 User Enrollment")
    print("=" * 60)
    
    name = input("\nEnter user name: ")
    role = input("Enter role (admin/manager/employee/guest): ")
    
    # Initialize components
    db = Database()
    camera = Camera({'index': 0})
    face_engine = FaceRecognitionEngine({'threshold': 0.6})
    
    print("\nCapturing face images...")
    print("Please look at the camera and press SPACE to capture (ESC to cancel)")
    
    captured = 0
    target = 5
    
    while captured < target:
        frame = camera.capture_frame()
        
        if frame is not None:
            cv2.imshow('Enrollment', frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 32:  # SPACE
                faces = camera.detect_faces(frame)
                if faces:
                    print(f"Captured {captured + 1}/{target}")
                    captured += 1
                else:
                    print("No face detected, try again")
            
            elif key == 27:  # ESC
                print("Enrollment cancelled")
                camera.release()
                cv2.destroyAllWindows()
                return
    
    camera.release()
    cv2.destroyAllWindows()
    
    print("\nEnrollment complete!")
    print(f"User '{name}' enrolled as {role}")

if __name__ == '__main__':
    enroll_user()
