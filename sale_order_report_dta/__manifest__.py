# encoding: utf-8
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Sale Order Report DTA",
    'version': "10.0.1.0.0",
    'author': "PESOL",
    'category': 'Customize',
    'description': """
This module allows add new sale order templates.
    """,
    'license': "AGPL-3",
    'depends': [
        'sale',
        'sale_layout_print_grouped',
        'sale_invoicing_method',
        'account_payment_partner'
    ],
    'data': [
        'views/report_saleorder.xml',
    ],
    'installable': True,
}
