# NeuroDoor-Pi5 Quick Start

## 🚀 Installation (4 Steps)

### 1. Extract and Navigate
```bash
tar -xzf neurodoor-pi5.tar.gz && cd neurodoor-pi5
```

### 2. Install
```bash
chmod +x setup.sh
sudo ./setup.sh install
```

### 3. Enroll First User (Admin)
```bash
source venv/bin/activate
python3 enroll_user.py
# Enter name and select 'admin' role
# Capture 5 face images
```

### 4. Start System
```bash
# Run in foreground
python3 main.py

# Or as service
sudo systemctl start neurodoor
sudo systemctl enable neurodoor
```

## 📊 Access Dashboard
Open: http://raspberrypi.local:5000

## ⚡ Quick Commands

```bash
# Check status
python3 main.py --status

# View access log
python3 main.py --log --days 7

# Unlock door
python3 main.py --unlock

# Emergency unlock
python3 main.py --emergency-unlock
```

## 🔧 Troubleshooting

### Camera Not Working
```bash
# Test camera
vcgencmd get_camera

# Check permissions
sudo usermod -a -G video $USER
```

### Door Lock Not Responding
```bash
# Test GPIO
python3 -c "from src.hardware import DoorLock; DoorLock().test()"

# Check permissions
sudo usermod -a -G gpio $USER
```

For full documentation, see README.md
