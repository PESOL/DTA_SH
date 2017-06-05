# -*- coding: utf-8 -*-

{
    "name": "Invoice line postion",
    "summary": "Show position field in invoice line",
    "version": "10.0.1.0.0",
    "category": "account",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'account',
    ],
    "data": [
        'views/account_invoice_position_view.xml',
    ]
}
