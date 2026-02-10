# Neuro Door Pi5 🚪🤖

An AI-assisted smart door access control system designed for Raspberry Pi 5. Combines computer vision with adaptive security logic to manage secure access dynamically through facial recognition and intelligent decision rules.

![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi%205-red.svg)

## 🌟 Features

### Core Functionality
- **AI-Powered Facial Recognition**
  - Real-time face detection and recognition
  - Multi-face processing
  - High accuracy (>95%) recognition
  - Anti-spoofing detection (liveness check)
  - Age estimation and gender detection

- **Adaptive Security Logic**
  - Time-based access rules
  - User role management
  - Dynamic authorization levels
  - Suspicious activity detection
  - Behavioral pattern analysis
  - Automatic threat assessment

- **Access Control**
  - Electronic door lock control
  - Multiple authentication modes
  - Two-factor authentication support
  - Temporary access codes
  - Guest management
  - Emergency override

### Advanced Features
- **Machine Learning**
  - Continuous learning from access patterns
  - Anomaly detection
  - User behavior modeling
  - Risk scoring algorithm
  - Adaptive threshold adjustment

- **Multi-Modal Authentication**
  - Facial recognition (primary)
  - PIN code (secondary)
  - RFID/NFC card support
  - Mobile app authentication
  - Voice recognition (optional)

- **Smart Notifications**
  - Real-time access alerts
  - Unusual activity warnings
  - Failed access attempts
  - System status updates
  - Email, SMS, and push notifications

- **Comprehensive Logging**
  - All access attempts logged
  - Photo capture for every event
  - Detailed audit trail
  - GDPR-compliant data handling
  - Exportable reports

## 📋 Hardware Requirements

### Essential Components

| Component | Specification | Purpose |
|-----------|--------------|---------|
| Microcontroller | Raspberry Pi 5 (8GB RAM recommended) | Main processing unit |
| Camera | Raspberry Pi Camera Module 3 or USB webcam | Face capture |
| Door Lock | Electronic Strike/Magnetic Lock (12V) | Physical access control |
| Relay Module | 5V Relay Module (10A+) | Lock control |
| Power Supply | 5V 5A for Pi + 12V for lock | System power |
| Display (Optional) | 7" Touchscreen | Local interface |
| Speaker | USB Speaker or 3.5mm | Audio feedback |
| Microphone (Optional) | USB Microphone | Voice commands |

### Optional Components
- RFID/NFC Reader (RC522 or PN532)
- PIR Motion Sensor
- Buzzer for audio alerts
- LED indicators (Red/Green)
- Keypad for PIN entry
- Backup battery (UPS)

### Wiring Diagram

```
Raspberry Pi 5 Connections:

Camera Module:
- Connect via CSI port

Relay Module (for door lock):
- VCC → 5V (Pin 2)
- GND → GND (Pin 6)
- IN  → GPIO 17 (Pin 11)

Door Lock (12V):
- Positive → Relay NO (Normally Open)
- Negative → 12V Power Supply GND
- 12V Power Supply → Relay Common

PIR Sensor (Optional):
- VCC → 5V (Pin 4)
- GND → GND (Pin 9)
- OUT → GPIO 27 (Pin 13)

Status LEDs:
- Green LED → GPIO 22 (Pin 15) + 220Ω resistor → GND
- Red LED → GPIO 23 (Pin 16) + 220Ω resistor → GND

Buzzer:
- Positive → GPIO 24 (Pin 18)
- Negative → GND (Pin 20)
```

## 🚀 Installation

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-dev git cmake \
    libopencv-dev python3-opencv libatlas-base-dev \
    libjasper-dev libqtgui4 libqt4-test libhdf5-dev

# Enable camera
sudo raspi-config
# Navigate to: Interface Options → Camera → Enable

# Reboot
sudo reboot
```

### 2. Clone Repository

```bash
git clone https://github.com/yourusername/neurodoor-pi5.git
cd neurodoor-pi5
```

### 3. Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Download face recognition models
python3 download_models.py
```

### 4. Initial Configuration

```bash
# Copy example configuration
cp config.example.yaml config.yaml

# Edit configuration
nano config.yaml

# Initialize database
python3 init_db.py
```

### 5. Register First User (Admin)

```bash
# Run enrollment wizard
python3 enroll_user.py

# Follow prompts:
# - Enter name
# - Select role (admin)
# - Capture face images (system will guide you)
# - Set PIN code
```

### 6. Run the System

```bash
# Start in foreground (testing)
python3 main.py

# Or install as service
sudo ./setup.sh install
sudo systemctl start neurodoor
sudo systemctl enable neurodoor
```

## 📖 Usage

### Web Dashboard

Access at: `http://raspberrypi.local:5000`

**Features:**
- Live camera feed
- Recent access log
- User management
- Access rules configuration
- System statistics
- Real-time alerts

**Default Credentials:**
- Username: admin
- Password: admin123 (change immediately!)

### User Enrollment

```bash
# Enroll new user
python3 enroll_user.py

# Enroll with photo
python3 enroll_user.py --photo /path/to/photo.jpg

# Bulk enrollment
python3 enroll_user.py --batch users.csv
```

### Access Control Modes

1. **Face Only** (Default)
   - Single-factor authentication
   - Fastest access
   - Suitable for low-security areas

2. **Face + PIN**
   - Two-factor authentication
   - Enhanced security
   - Recommended for restricted areas

3. **Face + Time-based**
   - Access restricted to specific hours
   - Automatic rule enforcement
   - Ideal for office environments

4. **Guest Mode**
   - Temporary access codes
   - Time-limited permissions
   - Automatic expiration

### Command Line Interface

```bash
# Check system status
python3 main.py --status

# View access log
python3 main.py --log --days 7

# Export report
python3 main.py --report --start-date 2024-01-01 --end-date 2024-01-31

# Test recognition
python3 main.py --test

# Unlock door manually
python3 main.py --unlock

# Lock door manually
python3 main.py --lock

# Emergency unlock
python3 main.py --emergency-unlock
```

## ⚙️ Configuration

### Security Settings (`config.yaml`)

```yaml
security:
  # Recognition thresholds
  face_recognition_threshold: 0.6  # Lower = stricter
  liveness_detection: true
  anti_spoofing: true
  
  # Access control
  max_failed_attempts: 3
  lockout_duration: 300  # seconds
  two_factor_required: false
  
  # Door lock
  unlock_duration: 5  # seconds
  auto_lock: true
  
  # Time restrictions
  enforce_time_rules: true
  business_hours:
    start: "08:00"
    end: "18:00"
```

### User Roles

| Role | Permissions | Description |
|------|-------------|-------------|
| **Admin** | Full access, user management, system config | System administrator |
| **Manager** | Access + limited user management | Department manager |
| **Employee** | Standard access during business hours | Regular employee |
| **Guest** | Temporary access only | Visitors |
| **Restricted** | Limited access, requires approval | Contractors |

### Access Rules

```yaml
access_rules:
  - name: "Office Hours"
    enabled: true
    applies_to: ["employee", "guest"]
    time_range:
      days: ["monday", "tuesday", "wednesday", "thursday", "friday"]
      start: "08:00"
      end: "18:00"
  
  - name: "24/7 Access"
    enabled: true
    applies_to: ["admin", "manager"]
    time_range: null  # No restrictions
  
  - name: "Weekend Restricted"
    enabled: true
    applies_to: ["guest"]
    days_blocked: ["saturday", "sunday"]
```

## 🤖 AI & Machine Learning

### Facial Recognition Model

- **Base Model**: face_recognition library (dlib-based)
- **Accuracy**: >95% under normal conditions
- **Speed**: ~0.5s per recognition on Pi 5
- **Training**: Requires minimum 5 photos per person

### Adaptive Security Logic

The system learns from access patterns:

1. **Normal Behavior Baseline**
   - Typical access times
   - Common entry patterns
   - Regular associates

2. **Anomaly Detection**
   - Unusual access times
   - Rapid successive attempts
   - Unknown face patterns
   - Multiple faces simultaneously

3. **Risk Scoring**
   - Real-time risk assessment
   - Confidence-based decisions
   - Escalation protocols

4. **Continuous Learning**
   - Face encoding updates
   - Pattern refinement
   - Threshold optimization

### Anti-Spoofing

Detects presentation attacks:
- Photo detection
- Video replay detection
- Mask detection
- 3D face liveness check

## 📊 Data Management

### Database Schema

```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    face_encoding BLOB,
    pin_hash TEXT,
    active BOOLEAN DEFAULT 1,
    created_at DATETIME,
    last_access DATETIME
);

-- Access log
CREATE TABLE access_log (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    timestamp DATETIME,
    success BOOLEAN,
    method TEXT,  -- face, pin, card, etc.
    confidence REAL,
    photo_path TEXT,
    risk_score REAL,
    anomaly_detected BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Access rules
CREATE TABLE access_rules (
    id INTEGER PRIMARY KEY,
    name TEXT,
    rule_type TEXT,
    parameters TEXT,  -- JSON
    enabled BOOLEAN
);
```

### Data Privacy

- **GDPR Compliant**: Right to deletion, data export
- **Encrypted Storage**: Face encodings encrypted at rest
- **Retention Policy**: Configurable data retention
- **Audit Trail**: Complete access history
- **Photo Management**: Automatic cleanup of old photos

### Data Export

```bash
# Export all data
python3 main.py --export-all

# Export specific date range
python3 main.py --export --start 2024-01-01 --end 2024-01-31

# Export for specific user
python3 main.py --export --user "John Doe"

# Export format: CSV, JSON, PDF
python3 main.py --export --format pdf
```

## 🔔 Alert System

### Alert Types

1. **Access Granted** (Info)
   - Successful recognition
   - User name and time
   - Confidence score

2. **Access Denied** (Warning)
   - Failed recognition
   - Unknown face
   - Unauthorized time

3. **Suspicious Activity** (Critical)
   - Multiple failed attempts
   - Anti-spoofing detection
   - Tailgating detected
   - Forced entry attempt

4. **System Alerts** (Info/Warning)
   - Low confidence recognition
   - Camera offline
   - Lock malfunction
   - System errors

### Notification Channels

```yaml
notifications:
  email:
    enabled: true
    recipients:
      - security@example.com
      - admin@example.com
  
  sms:
    enabled: true
    numbers:
      - "+1234567890"
  
  webhook:
    enabled: true
    url: "https://your-webhook.com/alerts"
  
  telegram:
    enabled: false
    bot_token: "YOUR_BOT_TOKEN"
    chat_id: "YOUR_CHAT_ID"
```

## 🎛️ Hardware Control

### Door Lock Control

```python
from src.hardware import DoorLock

lock = DoorLock()

# Unlock for 5 seconds
lock.unlock(duration=5)

# Permanent unlock
lock.unlock(permanent=True)

# Lock
lock.lock()

# Check status
status = lock.get_status()
print(f"Lock is {'locked' if status else 'unlocked'}")
```

### Camera Control

```python
from src.camera import Camera

camera = Camera()

# Capture frame
frame = camera.capture_frame()

# Detect faces
faces = camera.detect_faces(frame)

# Release camera
camera.release()
```

## 📱 Mobile Integration

### REST API Endpoints

```
GET  /api/status           - System status
GET  /api/users            - List users (admin only)
POST /api/users            - Add new user
GET  /api/access-log       - Access history
POST /api/unlock           - Remote unlock (admin only)
GET  /api/live-feed        - Camera stream
POST /api/authenticate     - Mobile authentication
```

### Mobile App Features

- Remote door unlock
- Live camera feed
- Access log viewing
- Real-time notifications
- Temporary access codes
- Guest management

## 🔧 Troubleshooting

### Camera Issues

```bash
# Test camera
vcgencmd get_camera

# List cameras
ls /dev/video*

# Test with fswebcam
sudo apt install fswebcam
fswebcam test.jpg

# Check camera permissions
sudo usermod -a -G video $USER
```

### Recognition Problems

1. **Low Accuracy**
   - Ensure good lighting
   - Capture more training photos
   - Clean camera lens
   - Adjust recognition threshold

2. **Slow Recognition**
   - Reduce image resolution
   - Enable hardware acceleration
   - Optimize face encoding database
   - Use faster detection model

3. **False Rejections**
   - Re-enroll with more varied photos
   - Lower recognition threshold
   - Update face encodings
   - Check for obstructions (glasses, masks)

### Lock Control Issues

```bash
# Test relay
python3 -c "from src.hardware import DoorLock; DoorLock().test()"

# Check GPIO permissions
sudo usermod -a -G gpio $USER

# Verify wiring
# Check relay LED indicator
# Test lock with direct power
```

### Service Issues

```bash
# Check status
sudo systemctl status neurodoor

# View logs
sudo journalctl -u neurodoor -f

# Restart service
sudo systemctl restart neurodoor

# Run in debug mode
python3 main.py --debug
```

## 🏗️ Project Structure

```
neurodoor-pi5/
│
├── main.py                    # Main application
├── enroll_user.py            # User enrollment utility
├── download_models.py        # Download face recognition models
├── init_db.py                # Database initialization
├── config.yaml               # Configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # Installation script
├── neurodoor.service         # Systemd service file
│
├── src/
│   ├── __init__.py
│   ├── camera.py             # Camera interface
│   ├── face_recognition.py   # Face recognition engine
│   ├── access_control.py     # Access control logic
│   ├── hardware.py           # Door lock & GPIO control
│   ├── ai_engine.py          # ML & adaptive security
│   ├── alerts.py             # Notification system
│   ├── database.py           # Database operations
│   ├── web_dashboard.py      # Flask web interface
│   └── api.py                # REST API
│
├── tests/                    # Unit tests
├── docs/                     # Documentation
├── logs/                     # Application logs
├── data/
│   ├── faces/               # User face images
│   ├── models/              # ML models
│   └── neurodoor.db         # SQLite database
│
├── static/                   # Web dashboard assets
└── templates/                # Web templates
```

## 🔒 Security Best Practices

1. **Change Default Passwords**
   - Web dashboard admin password
   - Database password (if applicable)

2. **Network Security**
   - Use HTTPS for web dashboard
   - Implement firewall rules
   - Disable unused services
   - Use VPN for remote access

3. **Physical Security**
   - Secure Raspberry Pi in tamper-proof enclosure
   - Backup power supply
   - Secure camera mounting
   - Protect wiring

4. **Data Security**
   - Regular backups
   - Encrypt face encodings
   - Secure API endpoints
   - Audit access logs

5. **Regular Maintenance**
   - Update face encodings monthly
   - Review access logs weekly
   - Test emergency procedures
   - Update software regularly

## 📈 Performance

- **Recognition Speed**: 0.3-0.7s per face
- **False Accept Rate**: <1%
- **False Reject Rate**: <5%
- **Maximum Users**: 1000+
- **Concurrent Faces**: Up to 5
- **Camera FPS**: 15-30
- **CPU Usage**: 30-50% during recognition
- **Memory Usage**: ~500MB

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Test face recognition
pytest tests/test_recognition.py

# Test access control
pytest tests/test_access_control.py

# Test with coverage
pytest --cov=src tests/

# Performance test
python3 tests/performance_test.py
```

