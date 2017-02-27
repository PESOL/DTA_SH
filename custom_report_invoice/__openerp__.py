# encoding: utf-8

{
    'name': "Custom Invoice Report",
    'version': "1.0",
    'author': "Angel Moya",
    'category': 'Customize',
    'description': """
Plantilla de factura por defecto
    """,
    'license': "AGPL-3",
    'depends': [
        'account',
        'custom_report_css'
    ],
    'data': [
        'views/report_invoice.xml',
    ],
    'installable': True,
}
