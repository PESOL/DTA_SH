# encoding: utf-8
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Base Layout Report DTA",
    'version': "10.0.1.0.0",
    'author': "PESOL",
    'category': 'Customize',
    'description': """
This module allows set the layout template.
    """,
    'license': "AGPL-3",
    'depends': [
        'report',
        'stock'
    ],
    'data': [
        'views/layouts.xml',
    ],
    'installable': True,
}
