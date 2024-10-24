# my_module/controllers/vendor_stock_update_controller.py
import jwt
import datetime
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessDenied

SECRET_KEY = 'my_secret_key'

class VendorStockUpdateController(http.Controller):

    def log_request(self, endpoint, payload, status, response_message):
        # Log the API request (success or failure)
        request.env['api.request.log'].sudo().create_log(endpoint, payload, status, response_message)

    def validate_jwt_token(self, token):
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return decoded_token  # If valid, return the payload
        except jwt.ExpiredSignatureError:
            raise AccessDenied('Token has expired')
        except jwt.InvalidTokenError:
            raise AccessDenied('Invalid token')

    @http.route('/vendor/stock_update', type='json', auth='public', methods=['POST'], csrf=False)
    def vendor_stock_update(self, **kwargs):
        token = request.httprequest.headers.get('Authorization')
        if not token:
            message = 'Token missing'
            self.log_request('/vendor/stock_update', kwargs, 'failed', message)
            return {'status': 'error', 'message': message}

        try:
            self.validate_jwt_token(token)
        except AccessDenied as e:
            message = str(e)
            self.log_request('/vendor/stock_update', kwargs, 'failed', message)
            return {'status': 'error', 'message': message}

        stock_updates = kwargs.get('stock_updates', [])
        
        for update in stock_updates:
            sku = update.get('sku')
            new_stock_qty = update.get('stock_qty')
            
            product = request.env['product.product'].sudo().search([('default_code', '=', sku)], limit=1)
            
            if product:
                product_variant = product.product_variant_ids[0]
                product_variant.sudo().write({'qty_available': new_stock_qty})
                product.message_post(body=f"Stock updated by vendor. New stock: {new_stock_qty}")
        
        # Log successful request
        self.log_request('/vendor/stock_update', kwargs, 'success', 'Stock updated successfully')
        
        return {'status': 'success', 'message': 'Stock updated successfully'}
