# -*- coding: utf-8 -*-
{
    "name": "Project Forecast Improve",
    "summary": "Forecast Improve",
    "version": "10.0.1.0.0",
    "category": "Project",
    "website": "http://www.pesol.es",
    "author": "PESOL",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        'project',
        'project_forecast',
        'hr_timesheet'
    ],
    "data": [
        # 'security/ir.model.access.csv',
        'views/project_forecast_view.xml'
    ]
}
