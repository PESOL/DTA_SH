# encoding: utf-8

from odoo import models, api, fields, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    supplier_product_code = fields.Char(
        compute='_compute_supplier_product_code')
    supplier_date_planned = fields.Date(
        compute='_compute_supplier_date_planned')

    @api.multi
    def _compute_supplier_product_code(self):
        for record in self:
            supplier_info = record.product_id.seller_ids.filtered(
                lambda s: s.name == record.order_id.partner_id
            )
            record.supplier_product_code = supplier_info \
                and supplier_info.product_code or ''

    @api.multi
    def _compute_supplier_date_planned(self):
        for record in self:
            record.supplier_date_planned = record.date_planned
