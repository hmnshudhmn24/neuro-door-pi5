"""Tests for access control"""
import sys
from datetime import datetime
sys.path.insert(0, '..')
from src.access_control import AccessController

def test_admin_access():
    """Test admin always has access"""
    controller = AccessController({'face_recognition_threshold': 0.6})
    user = {'id': 1, 'name': 'Admin', 'role': 'admin', 'active': True}
    result = controller.check_access(user, 0.9, datetime.now())
    assert result['granted'] == True

def test_low_confidence():
    """Test low confidence rejection"""
    controller = AccessController({'face_recognition_threshold': 0.6})
    user = {'id': 1, 'name': 'User', 'role': 'employee', 'active': True}
    result = controller.check_access(user, 0.3, datetime.now())
    assert result['granted'] == False
