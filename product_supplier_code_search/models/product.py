# -*- encoding: utf-8 -*-
from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_supplier_code = fields.Char(
        string='Supplier Code',
        compute='_compute_default_supplier_code')

    @api.multi
    def _compute_default_supplier_code(self):
        for product in self:
            product.default_supplier_code = product.seller_ids and (
                product.seller_ids[0].product_code
            )
