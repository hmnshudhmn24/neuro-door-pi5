"""Hardware Control Module"""
import logging
import time

logger = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    HAS_GPIO = True
except ImportError:
    HAS_GPIO = False
    logger.warning("GPIO not available, using simulation mode")

class DoorLock:
    """Door lock controller"""
    
    def __init__(self, pin=17):
        self.pin = pin
        self.simulation_mode = not HAS_GPIO
        self.locked = True
        
        if not self.simulation_mode:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.pin, GPIO.OUT)
            GPIO.output(self.pin, GPIO.LOW)
            logger.info(f"Door lock initialized on GPIO {self.pin}")
        else:
            logger.info("Door lock in simulation mode")
    
    def unlock(self, duration=5):
        """Unlock door for specified duration"""
        logger.info(f"Unlocking door for {duration}s")
        
        if not self.simulation_mode:
            GPIO.output(self.pin, GPIO.HIGH)
        
        self.locked = False
        
        if duration > 0:
            time.sleep(duration)
            self.lock()
    
    def lock(self):
        """Lock door"""
        logger.info("Locking door")
        
        if not self.simulation_mode:
            GPIO.output(self.pin, GPIO.LOW)
        
        self.locked = True
    
    def is_locked(self):
        """Check if door is locked"""
        return self.locked
    
    def test(self):
        """Test door lock"""
        logger.info("Testing door lock...")
        self.unlock(duration=2)
        logger.info("Door lock test complete")
