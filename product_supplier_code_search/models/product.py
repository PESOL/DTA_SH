# -*- encoding: utf-8 -*-
from odoo import models, api, fields


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    default_supplier_code_1 = fields.Char(
        string='Supplier Code',
        compute='_compute_default_supplier_code_1',
        store=True)

    @api.multi
    @api.depends('seller_ids')
    def _compute_default_supplier_code_1(self):
        for product in self:
            product.default_supplier_code_1 = product.seller_ids and (
                product.seller_ids[0].product_code
            ) or ''


class ProductProduct(models.Model):
    _inherit = 'product.product'

    default_supplier_code_2 = fields.Char(
        string='Supplier Code',
        compute='_compute_default_supplier_code_2',
        store=True)

    @api.multi
    @api.depends('seller_ids')
    def _compute_default_supplier_code_2(self):
        for product in self:
            product.default_supplier_code_2 = product.seller_ids and (
                product.seller_ids[0].product_code
            ) or ''
