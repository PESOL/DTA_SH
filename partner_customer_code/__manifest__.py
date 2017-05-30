# -*- coding: utf-8 -*-
{
    "name": "Partner Customer Code",
    "summary": "Custom field code in partner",
    "version": "10.0.1.0.0",
    "category": "Customers",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'base'
    ],
    "data": [
        'data/ir_sequence_data.xml',
        'views/partner_customer_view.xml',
    ]
}
