# my_module/__manifest__.py
{
    'name': 'API Request Logger',
    'version': '1.0',
    'summary': 'Logs and monitors API requests, including success and failures.',
    'description': """
        This module logs API requests to Odoo endpoints, including success and failure,
        and provides views to monitor the requests.
    """,
    'author': 'Your Name',
    'category': 'Custom',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/api_request_log_views.xml',
    ],
    'installable': True,
    'application': True,
}
