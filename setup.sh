#!/bin/bash
set -e

echo "======================================"
echo "NeuroDoor-Pi5 Setup"
echo "======================================"

install() {
    echo "Installing system dependencies..."
    sudo apt update
    sudo apt install -y python3-pip python3-dev cmake libopencv-dev python3-opencv
    
    echo "Setting up Python environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo "Creating directories..."
    mkdir -p logs data/faces data/models
    
    echo "Initializing database..."
    python3 init_db.py
    
    echo "Installing service..."
    INSTALL_DIR=$(pwd)
    cat > neurodoor.service << EOF
[Unit]
Description=NeuroDoor-Pi5 Access Control
After=network.target

[Service]
Type=simple
User=$SUDO_USER
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    
    sudo cp neurodoor.service /etc/systemd/system/
    sudo systemctl daemon-reload
    
    echo "Setup complete!"
}

case "$1" in
    install) install ;;
    *) echo "Usage: $0 install" ; exit 1 ;;
esac
