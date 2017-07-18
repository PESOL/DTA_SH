# encoding: utf-8
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, api, fields, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    position = fields.Char(
        string='Position')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    limit_date = fields.Char(
        string='Limit Date')

    report_type = fields.Selection(
        [('vehicle', 'Vehicle DTA'),
         ('refill', 'Refill'),
         ('represented', 'Represented')],
        string='Report Type',
        required=True)
