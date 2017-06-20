# -*- coding: utf-8 -*-

from odoo import models, api, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    margin_percent = fields.Float(
        string='Margin %')

    @api.onchange('margin_percent', 'purchase_price')
    def _onchange_margin(self):
        self.price_unit = self.purchase_price * (
            1 + (self.margin_percent / 100))

    @api.onchange('price_unit')
    def _onchange_price_unit(self):
        if self.price_unit:
            self.margin_percent = (
                (self.price_unit - self.purchase_price) * 100
            ) / self.purchase_price

    @api.model
    def create(self, values):
        purchase_price = values.get('purchase_price')
        price_unit = values.get('price_unit')
        if purchase_price and price_unit:
            margin_percent = ((price_unit - purchase_price) * 100
                              ) / purchase_price
            values.update({
                'margin_percent': margin_percent})
        return super(SaleOrderLine, self).create(values)
