# -*- coding: utf-8 -*-
# Copyright 2017 Pesol (<http://pesol.es>)
#                Angel Moya <angel.moya@pesol.es>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)


{
    'name': 'Website Document Page',
    'version': '10.0.1.0.0',
    'category': 'Knowledge',
    'license': 'AGPL-3',
    'author': "PESOL, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/oca/contract',
    'depends': ['document_page', 'website'],
    'data': [
        'views/website_document_page_templates.xml',
        'views/document_page.xml'
    ],
    'installable': True,
}
