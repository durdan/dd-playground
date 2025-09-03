from flask import Flask, request, jsonify, g
from admin_middleware import admin_middleware
from auth_service import AuthService

app = Flask(__name__)
auth_service = AuthService()

@app.route('/login', methods=['POST'])
def login():
    """Login endpoint to get JWT token"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'JSON data required'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    try:
        token = auth_service.authenticate(username, password)
        if not token:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        return jsonify({'token': token}), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/admin/users', methods=['GET'])
@admin_middleware.require_admin
def get_users():
    """Protected admin endpoint"""
    return jsonify({
        'message': 'Admin access granted',
        'current_user': g.current_user,
        'users': ['admin', 'user']
    })

@app.route('/admin/settings', methods=['POST'])
@admin_middleware.require_admin
def update_settings():
    """Another protected admin endpoint"""
    return jsonify({
        'message': 'Settings updated successfully',
        'updated_by': g.current_user['username']
    })

@app.route('/public', methods=['GET'])
def public_endpoint():
    """Public endpoint - no authentication required"""
    return jsonify({'message': 'This is a public endpoint'})

if __name__ == '__main__':
    app.run(debug=True)