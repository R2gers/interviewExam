from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# Mock Database
machine_data = {
    "status": "IDLE",
    "name": 'DummyMachine',
    "status_history": []
}

VALID_STATUSES = {"IDLE", "STARTED", "COMPLETED"}

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(machine_data)

@app.route('/status', methods=['POST'])
def update_status():
    data = request.json

    if not data or 'status' not in data:
        return jsonify({'error': 'Status field is required'}), 400
    
    new_status = data['status'].upper()
    
    if new_status not in VALID_STATUSES:
        return jsonify({
            'error': f'Invalid status. Must be one of: {", ".join(VALID_STATUSES)}'
        }), 400
    
    old_status = machine_data['status']
    machine_data['status'] = new_status
    
    machine_data['status_history'].append({
        'timestamp': datetime.now().isoformat(),
        'old_status': old_status,
        'new_status': new_status
    })
    
    return jsonify({
        'message': 'Status updated successfully',
        'current_status': new_status
    })

if __name__ == '__main__':
    app.run(debug=True)