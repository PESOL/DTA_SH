# -*- coding: utf-8 -*-
{
    "name": "Sale Layout Print Grouped",
    "summary": "Print layout sales",
    "version": "10.0.1.0.0",
    "category": "CRM",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'crm',
        'sale'
    ],
    "data": [
        'views/sale_layout_category_view.xml',
        'views/sale_layout_template.xml',
        'views/sale_order_view.xml'
    ]
}
