# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class PurchaseRequirement(models.Model):
    _name = 'purchase.requirement'

    name = fields.Char(
        string='Description',
        required=True)

    ref = fields.Char(
        string='Ref')

    state = fields.Selection(
        [('pending', 'Pending'),
         ('reviwed', 'Reviwed'),
         ('in_process', 'In Process')],
        string='State',
        track_visibility='onchange',
        required=True,
        copy=False,
        default="pending")

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product')

    product_qty = fields.Float(
        string='Product Qty')

    required_date = fields.Date(
        string='Required Date',
        required=True)

    supplier_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='purchase_req_partner',
        column1='partner_id',
        column2='supplier_id',
        string='Partner')

    purchase_order_ids = fields.One2many(
        comodel_name='purchase.order',
        inverse_name='purchase_requirement_id',
        string='Purchase Order')

    @api.multi
    def generate_sales(self):
        purchase_order_obj = self.env['purchase.order']
        self.state = 'in_process'
        orders_values = {}
        for requirement in self.filtered('supplier_ids'):
            order_line = {
                'product_id': requirement.product_id.id,
                'name': requirement.name,
                'date_planned': requirement.required_date,
                'product_qty': requirement.product_qty,
                'product_uom':
                    requirement.product_id.product_tmpl_id.uom_id.id,
                'price_unit': requirement.product_id.standard_price
            }
            for partner in requirement.supplier_ids:
                if partner.id in orders_values.keys():
                    orders_values[partner.id].append((0, 0, order_line))
                else:
                    orders_values.update({
                        partner.id: [(0, 0, order_line)]
                    })
        for partner_id in orders_values.keys():
            purchase_order_obj.create({
                'partner_id': partner_id,
                'order_line': order_line
            })

    @api.onchange('product_id')
    def _onchange_product_id(self):
        self.name = self.product_id.name
        if self.product_id.default_code:
            self.ref = self.product_id.default_code


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_requirement_id = fields.Many2one(
        comodel_name='purchase.requirement',
        string='Purchase Requirement')


class project(models.Model):
    _inherit = 'project.project'
