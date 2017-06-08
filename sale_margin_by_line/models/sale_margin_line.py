# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_percent = fields.Float(
        string='Margin %')

    @api.onchange('margin_percent')
    def _onchange_margin(self):
        self.price_unit = self.purchase_price * (
            1 + (self.margin_percent / 100))

    @api.onchange('price_unit', 'purchase_price')
    def _onchange_price_unit(self):
        self.margin_percent = (
            (self.price_unit - self.purchase_price) * 100
        ) / self.purchase_price
