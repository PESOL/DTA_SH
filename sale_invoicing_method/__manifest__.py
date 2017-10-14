# -*- coding: utf-8 -*-
{
    "name": "Sale Invoicing Method",
    "summary": "sale invoicing method",
    "version": "10.0.1.0.0",
    "category": "Sales",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'sale'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/sale_invoicing_view.xml',
    ]
}
