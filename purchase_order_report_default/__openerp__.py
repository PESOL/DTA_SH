# encoding: utf-8
{
    'name': "Purchase Order Report Default",
    'version': "9.0.1.0.0",
    'author': "PESOL",
    'category': 'Custom Reporting',
    'license': "AGPL-3",
    'depends': [
        'purchase'
    ],
    'data': [
        'views/purchase_order_templates.xml',
        'views/purchase_quotation_templates.xml',
    ],
    'installable': True,
}
