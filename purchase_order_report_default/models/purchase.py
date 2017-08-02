# encoding: utf-8

from odoo import models, api, fields, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    supplier_code = fields.Char(
        string='Supplier Code')


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    supplier_date_planned = fields.Date(
        compute='_compute_supplier_date_planned')

    needed_dta_date = fields.Char(
        string='Needed DTA Date')

    supplier_deadline = fields.Char(
        string='Supplier Deadline')


    @api.multi
    def _compute_supplier_date_planned(self):
        for record in self:
            record.supplier_date_planned = record.date_planned
