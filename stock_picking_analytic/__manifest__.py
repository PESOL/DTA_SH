# encoding: utf-8
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Stock Picking Analytic",
    'version': "10.0.1.0.0",
    'author': "PESOL",
    'category': 'Customize',
    'description': """
This module allows add account analytic lines in pickings.
    """,
    'license': "AGPL-3",
    'depends': [
        'account',
        'analytic',
        'purchase',
        'stock',
    ],
    'data': [
        'views/stock_move_analytic_view.xml',
        'views/stock_quant_analytic_view.xml',
        'views/stock_picking_analytic_view.xml'
    ],
    'installable': True,
}
