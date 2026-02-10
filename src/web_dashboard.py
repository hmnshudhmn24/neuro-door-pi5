"""Web Dashboard Module"""
from flask import Flask, render_template_string, jsonify, request
import logging

logger = logging.getLogger(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>NeuroDoor-Pi5 Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        header { text-align: center; color: white; margin-bottom: 30px; }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-active { background: #10b981; }
        .status-inactive { background: #ef4444; }
        .log-entry {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            border-left: 3px solid;
        }
        .log-success { background: #d4edda; border-left-color: #28a745; }
        .log-failure { background: #f8d7da; border-left-color: #dc3545; }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            margin: 5px;
        }
        .btn-primary { background: #667eea; color: white; }
        .btn-danger { background: #dc3545; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚪🤖 NeuroDoor-Pi5</h1>
            <div>AI-Assisted Smart Door Access Control</div>
        </header>
        
        <div class="dashboard">
            <div class="card">
                <h2>System Status</h2>
                <p><span class="status-indicator status-active"></span>Camera: <span id="camera-status">Active</span></p>
                <p><span class="status-indicator status-active"></span>Lock: <span id="lock-status">Locked</span></p>
                <p>Total Users: <span id="user-count">0</span></p>
                <div style="margin-top: 20px;">
                    <button class="btn btn-primary" onclick="unlockDoor()">Unlock Door</button>
                    <button class="btn btn-danger" onclick="lockDoor()">Lock Door</button>
                </div>
            </div>
            
            <div class="card">
                <h2>Recent Access</h2>
                <div id="access-log">Loading...</div>
            </div>
        </div>
    </div>
    
    <script>
        async function updateStatus() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                document.getElementById('camera-status').textContent = data.camera || 'Unknown';
                document.getElementById('lock-status').textContent = data.door_lock || 'Unknown';
                document.getElementById('user-count').textContent = data.total_users || 0;
                
                const log = data.recent_access || [];
                const logHtml = log.map(entry => {
                    const cls = entry.success ? 'log-success' : 'log-failure';
                    const user = entry.user_name || 'Unknown';
                    return `<div class="log-entry ${cls}">${entry.timestamp} - ${user} (${entry.method})</div>`;
                }).join('');
                document.getElementById('access-log').innerHTML = logHtml || '<p>No recent activity</p>';
            } catch (error) {
                console.error('Error updating status:', error);
            }
        }
        
        async function unlockDoor() {
            await fetch('/api/unlock', { method: 'POST' });
            alert('Door unlocked');
        }
        
        async function lockDoor() {
            await fetch('/api/lock', { method: 'POST' });
            alert('Door locked');
        }
        
        updateStatus();
        setInterval(updateStatus, 5000);
    </script>
</body>
</html>
"""

def create_app(neurodoor):
    app = Flask(__name__)
    app.config['neurodoor'] = neurodoor
    
    @app.route('/')
    def index():
        return render_template_string(HTML_TEMPLATE)
    
    @app.route('/api/status')
    def get_status():
        try:
            status = neurodoor.get_status()
            return jsonify(status)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/unlock', methods=['POST'])
    def unlock():
        try:
            neurodoor.unlock_door(user='web')
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/lock', methods=['POST'])
    def lock():
        try:
            neurodoor.lock_door(user='web')
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return app
