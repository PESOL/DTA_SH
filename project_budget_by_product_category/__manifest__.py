# -*- coding: utf-8 -*-
{
    "name": "Project Budget By Product Category",
    "summary": "Cost forecast",
    "version": "10.0.1.0.0",
    "category": "CRM or Project",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'project',
        'sale',
        'crm'
    ],
    "data": [
        'views/project_budget_view.xml'
    ]
}
