# encoding: utf-8

from odoo import models, api, fields, _


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    supplier_date_planned = fields.Date(
        compute='_compute_supplier_date_planned')

    needed_dta_date = fields.Char(
        string='Needed DTA Date')

    supplier_deadline = fields.Char(
        string='field_name')

    @api.multi
    def _compute_supplier_date_planned(self):
        for record in self:
            record.supplier_date_planned = record.date_planned
