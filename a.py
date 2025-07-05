from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Validate email format
def is_valid_email(email):
    import re
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

# Validate phone number (10 digits)
def is_valid_phone(phone):
    import re
    pattern = r'^[0-9]{10}$'
    return re.match(pattern, phone.replace('-', '').replace(' ', '')) is not None

@app.route('/api/intern', methods=['POST'])
def register_intern():
    try:
        data = request.get_json()
        
        # Extract form data
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        college = data.get('college')
        internship = data.get('internship')
        mode = data.get('mode')
        discount_applied = data.get('discount_applied')

        # Validate required fields
        if not all([name, email, phone, college, internship, mode, discount_applied]):
            return jsonify({'error': 'All fields are required'}), 400

        # Validate email
        if not is_valid_email(email):
            return jsonify({'error': 'Invalid email address'}), 400

        # Validate phone
        if not is_valid_phone(phone):
            return jsonify({'error': 'Invalid phone number'}), 400

        # Validate internship program
        valid_programs = [
            'python', 'java', 'machine-learning', 'deep-learning',
            'generative-ai', 'agentic-ai', 'full-stack'
        ]
        if internship not in valid_programs:
            return jsonify({'error': 'Invalid internship program'}), 400

        # Validate mode
        valid_modes = ['online', 'offline']
        if mode not in valid_modes:
            return jsonify({'error': 'Invalid mode of internship'}), 400

        # Prepare data to store
        registration_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'college': college,
            'internship': internship,
            'mode': mode,
            'discount_applied': discount_applied,
            'created_at': datetime.now().isoformat()
        }

        # Append to response.json
        file_path = 'response.json'
        try:
            # Read existing data if file exists
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    try:
                        existing_data = json.load(file)
                        if not isinstance(existing_data, list):
                            existing_data = []
                    except json.JSONDecodeError:
                        existing_data = []
            else:
                existing_data = []

            # Append new registration
            existing_data.append(registration_data)

            # Write back to file
            with open(file_path, 'w') as file:
                json.dump(existing_data, file, indent=4)

        except Exception as e:
            return jsonify({'error': f'Failed to save registration: {str(e)}'}), 500

        return jsonify({'message': 'Registration successful'}), 200

    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)