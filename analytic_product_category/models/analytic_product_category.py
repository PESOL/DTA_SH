# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class AnalyticProductCategory(models.Model):
    _inherit = 'account.analytic.line'

    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category',
        related='product_id.categ_id',
        store=True)
