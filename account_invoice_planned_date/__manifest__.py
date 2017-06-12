# -*- coding: utf-8 -*-

{
    "name": "Account Invoice Planned Date",
    "summary": "add planned date field in the invoice",
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
        'views/account_invoice_planned_date_view.xml',
    ]
}
