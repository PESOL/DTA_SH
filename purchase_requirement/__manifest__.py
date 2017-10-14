# -*- coding: utf-8 -*-
{
    "name": "Purchase Requirement",
    "summary": "Shopping needs",
    "version": "10.0.1.0.0",
    "category": "CRM or Project",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'purchase'
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/purchase_requirement_view.xml',
        'views/purchase_order_view.xml',
        'wizard/purchase_requirement_wizard.xml'
    ]
}
