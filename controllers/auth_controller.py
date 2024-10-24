# my_module/controllers/auth_controller.py
import jwt
import datetime
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

SECRET_KEY = 'my_secret_key'

class AuthController(http.Controller):
    
    @http.route('/api/login', type='json', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        
        # Authenticate user
        user = request.env['res.users'].sudo().search([('login', '=', username)], limit=1)
        
        if user and user.check_password(password):
            # Generate JWT token
            payload = {
                'user_id': user.id,
                'exp': datetime.datetime.utc() + datetime.timedelta(hours=24),  # Token expires in 24 hours
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return {
                'status': 'success',
                'token': token,
                'message': 'Login successful'
            }
        
        return {
            'status': 'error',
            'message': 'Invalid credentials'
        }
