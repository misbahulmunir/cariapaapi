# my_module/models/api_request_log.py
from odoo import models, fields, api
import json

class APIRequestLog(models.Model):
    _name = 'api.request.log'
    _description = 'API Request Log'
    _order = 'create_date desc'

    name = fields.Char(string="Endpoint", required=True)
    request_payload = fields.Text(string="Request Payload")
    status = fields.Selection([
        ('success', 'Success'),
        ('failed', 'Failed')
    ], string="Status", required=True)
    response_message = fields.Text(string="Response Message")
    request_date = fields.Datetime(string="Request Date", default=fields.Datetime.now)

    @api.model
    def create_log(self, endpoint, payload, status, response_message):
        self.create({
            'name': endpoint,
            'request_payload': json.dumps(payload),
            'status': status,
            'response_message': response_message
        })
