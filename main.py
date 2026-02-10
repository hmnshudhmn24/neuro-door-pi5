#!/usr/bin/env python3
"""
NeuroDoor-Pi5 - AI-Assisted Smart Door Access Control
Main Application Entry Point
"""

import argparse
import sys
import signal
import time
import logging
from pathlib import Path
from datetime import datetime, timedelta
import yaml

from src.camera import Camera
from src.face_recognition import FaceRecognitionEngine
from src.access_control import AccessController
from src.hardware import DoorLock
from src.ai_engine import AIEngine
from src.alerts import AlertManager
from src.database import Database
from src.web_dashboard import create_app

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/neurodoor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class NeuroDoor:
    """Main NeuroDoor system controller"""
    
    def __init__(self, config_path='config.yaml'):
        """Initialize NeuroDoor system"""
        self.running = False
        self.config = self.load_config(config_path)
        
        logger.info("Initializing NeuroDoor-Pi5 system...")
        
        try:
            # Initialize components
            self.database = Database(self.config['database']['path'])
            self.camera = Camera(self.config['camera'])
            self.face_engine = FaceRecognitionEngine(self.config['recognition'])
            self.access_controller = AccessController(self.config['security'])
            self.door_lock = DoorLock(self.config['hardware']['lock_pin'])
            self.ai_engine = AIEngine(self.config['ai'])
            self.alert_manager = AlertManager(self.config['alerts'])
            
            logger.info("System initialization complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize system: {e}")
            raise
    
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            sys.exit(1)
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML configuration: {e}")
            sys.exit(1)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info("Shutdown signal received")
        self.stop()
    
    def start(self):
        """Start the access control system"""
        self.running = True
        logger.info("Starting NeuroDoor access control system...")
        
        # Register signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        try:
            while self.running:
                try:
                    # Capture frame from camera
                    frame = self.camera.capture_frame()
                    
                    if frame is None:
                        consecutive_errors += 1
                        logger.warning(f"Failed to capture frame ({consecutive_errors}/{max_consecutive_errors})")
                        
                        if consecutive_errors >= max_consecutive_errors:
                            self.alert_manager.send_alert({
                                'type': 'system_error',
                                'severity': 'critical',
                                'message': 'Camera failure - unable to capture frames',
                                'timestamp': datetime.now()
                            })
                            consecutive_errors = 0
                        
                        time.sleep(1)
                        continue
                    
                    # Detect faces in frame
                    faces = self.camera.detect_faces(frame)
                    
                    if faces:
                        for face in faces:
                            # Perform facial recognition
                            result = self.face_engine.recognize_face(frame, face)
                            
                            if result['user_id']:
                                user = self.database.get_user(result['user_id'])
                                
                                # Check access permissions
                                access_decision = self.access_controller.check_access(
                                    user=user,
                                    confidence=result['confidence'],
                                    timestamp=datetime.now()
                                )
                                
                                # AI risk assessment
                                risk_score = self.ai_engine.assess_risk(
                                    user=user,
                                    access_history=self.database.get_user_access_history(user['id']),
                                    current_context={'confidence': result['confidence']}
                                )
                                
                                # Log access attempt
                                log_entry = {
                                    'user_id': user['id'],
                                    'timestamp': datetime.now(),
                                    'success': access_decision['granted'],
                                    'method': 'face',
                                    'confidence': result['confidence'],
                                    'risk_score': risk_score,
                                    'anomaly_detected': risk_score > 0.7,
                                    'reason': access_decision.get('reason', '')
                                }
                                
                                self.database.log_access(log_entry)
                                
                                # Handle access decision
                                if access_decision['granted']:
                                    logger.info(f"Access GRANTED for {user['name']} (confidence: {result['confidence']:.2f})")
                                    
                                    # Unlock door
                                    self.door_lock.unlock(duration=self.config['security']['unlock_duration'])
                                    
                                    # Send notification
                                    self.alert_manager.send_alert({
                                        'type': 'access_granted',
                                        'severity': 'info',
                                        'message': f"Access granted to {user['name']}",
                                        'user': user['name'],
                                        'confidence': result['confidence'],
                                        'timestamp': datetime.now()
                                    })
                                    
                                else:
                                    logger.warning(f"Access DENIED for {user['name']} - {access_decision['reason']}")
                                    
                                    self.alert_manager.send_alert({
                                        'type': 'access_denied',
                                        'severity': 'warning',
                                        'message': f"Access denied to {user['name']}: {access_decision['reason']}",
                                        'user': user['name'],
                                        'reason': access_decision['reason'],
                                        'timestamp': datetime.now()
                                    })
                                
                                # Check for anomalies
                                if risk_score > 0.7:
                                    self.alert_manager.send_alert({
                                        'type': 'suspicious_activity',
                                        'severity': 'critical',
                                        'message': f"High risk score ({risk_score:.2f}) detected for {user['name']}",
                                        'user': user['name'],
                                        'risk_score': risk_score,
                                        'timestamp': datetime.now()
                                    })
                            
                            else:
                                # Unknown face
                                logger.warning("Unknown face detected")
                                
                                # Log unknown access attempt
                                self.database.log_access({
                                    'user_id': None,
                                    'timestamp': datetime.now(),
                                    'success': False,
                                    'method': 'face',
                                    'confidence': result['confidence'],
                                    'reason': 'Unknown face'
                                })
                                
                                self.alert_manager.send_alert({
                                    'type': 'unknown_face',
                                    'severity': 'warning',
                                    'message': 'Unknown face detected at door',
                                    'timestamp': datetime.now()
                                })
                        
                        consecutive_errors = 0
                    
                    # Small delay to reduce CPU usage
                    time.sleep(0.1)
                
                except Exception as e:
                    logger.error(f"Error in main loop: {e}", exc_info=True)
                    consecutive_errors += 1
                    time.sleep(1)
        
        finally:
            self.cleanup()
    
    def stop(self):
        """Stop the system"""
        logger.info("Stopping NeuroDoor system...")
        self.running = False
    
    def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up resources...")
        try:
            self.camera.release()
            self.database.close()
            logger.info("Cleanup complete")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    def get_status(self):
        """Get current system status"""
        try:
            return {
                'status': 'operational' if self.running else 'stopped',
                'camera': 'active' if self.camera.is_active() else 'inactive',
                'door_lock': 'locked' if self.door_lock.is_locked() else 'unlocked',
                'total_users': self.database.get_user_count(),
                'recent_access': self.database.get_recent_access(limit=5),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def unlock_door(self, duration=5, user='manual'):
        """Manually unlock door"""
        logger.info(f"Manual unlock requested by {user}")
        self.door_lock.unlock(duration=duration)
        
        # Log manual unlock
        self.database.log_access({
            'user_id': None,
            'timestamp': datetime.now(),
            'success': True,
            'method': 'manual',
            'reason': f'Manual unlock by {user}'
        })
    
    def lock_door(self, user='manual'):
        """Manually lock door"""
        logger.info(f"Manual lock requested by {user}")
        self.door_lock.lock()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='NeuroDoor-Pi5 - AI-Assisted Smart Door Access Control'
    )
    
    parser.add_argument('--config', default='config.yaml', help='Configuration file')
    parser.add_argument('--status', action='store_true', help='Display system status')
    parser.add_argument('--log', action='store_true', help='View access log')
    parser.add_argument('--days', type=int, default=7, help='Days of log history')
    parser.add_argument('--report', action='store_true', help='Generate report')
    parser.add_argument('--start-date', help='Report start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='Report end date (YYYY-MM-DD)')
    parser.add_argument('--test', action='store_true', help='Test recognition')
    parser.add_argument('--unlock', action='store_true', help='Unlock door')
    parser.add_argument('--lock', action='store_true', help='Lock door')
    parser.add_argument('--emergency-unlock', action='store_true', help='Emergency unlock')
    parser.add_argument('--web', action='store_true', help='Start web dashboard')
    parser.add_argument('--port', type=int, default=5000, help='Web port')
    parser.add_argument('--debug', action='store_true', help='Debug mode')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        neurodoor = NeuroDoor(args.config)
    except Exception as e:
        logger.error(f"Failed to initialize: {e}")
        sys.exit(1)
    
    if args.status:
        status = neurodoor.get_status()
        print("\n=== NeuroDoor-Pi5 Status ===")
        print(f"System: {status['status']}")
        print(f"Camera: {status.get('camera', 'unknown')}")
        print(f"Door Lock: {status.get('door_lock', 'unknown')}")
        print(f"Total Users: {status.get('total_users', 0)}")
        print(f"Timestamp: {status['timestamp']}")
        print("=" * 30 + "\n")
    
    elif args.log:
        start_date = datetime.now() - timedelta(days=args.days)
        logs = neurodoor.database.get_access_log(start_date=start_date, limit=50)
        print(f"\n=== Access Log (Last {args.days} days) ===\n")
        for log in logs:
            status = "✓" if log['success'] else "✗"
            user = log.get('user_name', 'Unknown')
            print(f"{status} {log['timestamp']} - {user} ({log['method']}) - {log.get('reason', '')}")
        print()
    
    elif args.unlock:
        neurodoor.unlock_door(user='CLI')
        print("Door unlocked")
    
    elif args.lock:
        neurodoor.lock_door(user='CLI')
        print("Door locked")
    
    elif args.emergency_unlock:
        neurodoor.unlock_door(duration=0, user='EMERGENCY')
        print("Emergency unlock activated - door will remain unlocked")
    
    elif args.web:
        app = create_app(neurodoor)
        logger.info(f"Starting web dashboard on port {args.port}")
        app.run(host='0.0.0.0', port=args.port, debug=args.debug)
    
    else:
        logger.info("=" * 60)
        logger.info("NeuroDoor-Pi5 - AI-Assisted Smart Door Access Control")
        logger.info("=" * 60)
        neurodoor.start()


if __name__ == '__main__':
    main()
