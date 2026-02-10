"""AI Engine for Adaptive Security"""
import logging
import numpy as np
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class AIEngine:
    """AI-powered adaptive security engine"""
    
    def __init__(self, config):
        self.config = config
        self.learning_enabled = config.get('learning_enabled', True)
    
    def assess_risk(self, user, access_history, current_context):
        """Calculate risk score for access attempt"""
        risk_score = 0.0
        
        # Analyze time patterns
        if access_history:
            normal_hours = self._get_normal_hours(access_history)
            current_hour = datetime.now().hour
            
            if current_hour not in normal_hours:
                risk_score += 0.3
        
        # Check confidence level
        confidence = current_context.get('confidence', 1.0)
        if confidence < 0.7:
            risk_score += 0.2
        
        # Detect rapid successive attempts
        recent_attempts = [a for a in access_history if 
                          (datetime.now() - datetime.fromisoformat(a['timestamp'])).seconds < 60]
        if len(recent_attempts) > 3:
            risk_score += 0.4
        
        return min(risk_score, 1.0)
    
    def _get_normal_hours(self, access_history):
        """Determine normal access hours from history"""
        hours = [datetime.fromisoformat(a['timestamp']).hour 
                for a in access_history if a.get('success')]
        return set(hours) if hours else set(range(8, 18))
    
    def detect_anomaly(self, user, current_access):
        """Detect anomalous access patterns"""
        # Placeholder for ML-based anomaly detection
        return False
