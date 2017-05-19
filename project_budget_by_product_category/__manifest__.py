# -*- coding: utf-8 -*-
{
    "name": "Project Budget By Product Category",
    "summary": "Cost forecast",
    "version": "10.0.1.0.0",
    "category": "Project",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'project',
        'sale_margin',
        'analytic_product_category'
    ],
    "data": [
        'views/project_budget_view.xml',
        'security/ir.model.access.csv'
    ]
}
