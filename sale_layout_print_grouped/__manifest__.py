# -*- coding: utf-8 -*-
{
    "name": "Sale Layout Print Grouped",
    "summary": "Print layout sales",
    "version": "10.0.1.0.0",
    "category": "Sales",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'sale',
        'website_quote',
        'account'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/account_invoice_layout_category_view.xml',
        'views/account_invoice_template.xml',
        'views/account_invoice_view.xml',
        'views/sale_layout_category_view.xml',
        'views/sale_layout_template.xml',
        'views/sale_order_view.xml',
        'views/sale_layout_template_sections_view.xml',
        'views/sale_order_layout_category_view.xml',
        'wizards/set_template_view.xml'
    ]
}
