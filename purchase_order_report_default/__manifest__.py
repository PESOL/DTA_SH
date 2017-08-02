# encoding: utf-8
{
    'name': "Purchase Order Report Default",
    'version': "10.0.1.0.0",
    'author': "PESOL",
    'category': 'Custom Reporting',
    'license': "AGPL-3",
    'depends': [
        'purchase_requirement'
    ],
    'data': [
        'views/purchase_order_templates.xml',
        'views/purchase_quotation_templates.xml',
        'views/purchase_quotation_view.xml'
    ],
    'installable': True,
}
