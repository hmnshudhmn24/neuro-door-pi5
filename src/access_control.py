"""Access Control Logic"""
import logging
from datetime import datetime, time

logger = logging.getLogger(__name__)

class AccessController:
    """Manages access control decisions"""
    
    def __init__(self, config):
        self.config = config
        self.threshold = config.get('face_recognition_threshold', 0.6)
        self.two_factor_required = config.get('two_factor_required', False)
        self.enforce_time_rules = config.get('enforce_time_rules', True)
    
    def check_access(self, user, confidence, timestamp):
        """Check if access should be granted"""
        
        # Check if user is active
        if not user.get('active', True):
            return {'granted': False, 'reason': 'User account disabled'}
        
        # Check recognition confidence
        if confidence < self.threshold:
            return {'granted': False, 'reason': 'Low recognition confidence'}
        
        # Check time-based rules
        if self.enforce_time_rules:
            if not self._check_time_rules(user, timestamp):
                return {'granted': False, 'reason': 'Outside allowed time'}
        
        # Check role-based rules
        if not self._check_role_rules(user):
            return {'granted': False, 'reason': 'Insufficient permissions'}
        
        return {'granted': True, 'reason': 'Access approved'}
    
    def _check_time_rules(self, user, timestamp):
        """Check time-based access rules"""
        current_time = timestamp.time()
        current_day = timestamp.strftime('%A').lower()
        
        role = user.get('role', 'guest')
        
        # Admins have 24/7 access
        if role == 'admin':
            return True
        
        # Business hours for employees
        if role == 'employee':
            if current_day in ['saturday', 'sunday']:
                return False
            if time(8, 0) <= current_time <= time(18, 0):
                return True
            return False
        
        return True
    
    def _check_role_rules(self, user):
        """Check role-based rules"""
        role = user.get('role', 'guest')
        return role in ['admin', 'manager', 'employee', 'guest']
