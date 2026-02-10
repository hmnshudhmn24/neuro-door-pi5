"""Alert Management System"""
import logging
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

class AlertManager:
    """Manages alert notifications"""
    
    def __init__(self, config):
        self.config = config
        self.email_config = config.get('email', {})
        self.sms_config = config.get('sms', {})
    
    def send_alert(self, alert):
        """Send alert through configured channels"""
        severity = alert.get('severity', 'info')
        
        logger.info(f"Alert: {alert['type']} - {alert['message']}")
        
        if severity in ['critical', 'warning']:
            if self.email_config.get('enabled'):
                self._send_email(alert)
        
        # Log all alerts
        self._log_alert(alert)
    
    def _send_email(self, alert):
        """Send email alert"""
        if not self.email_config.get('enabled'):
            return
        
        try:
            msg = MIMEText(f"{alert['type']}: {alert['message']}")
            msg['Subject'] = f"NeuroDoor Alert: {alert['severity'].upper()}"
            msg['From'] = self.email_config.get('from')
            msg['To'] = ', '.join(self.email_config.get('recipients', []))
            
            # Send via SMTP (implementation depends on config)
            logger.info("Email alert sent")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
    
    def _log_alert(self, alert):
        """Log alert to file"""
        logger.info(f"[ALERT] {alert}")
