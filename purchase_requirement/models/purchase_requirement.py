# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class PurchaseRequirement(models.Model):
    _name = 'purchase.requirement'

    name = fields.Char(
        string='Description')

    ref = fields.Char(
        string='Ref')

    state = fields.Selection(
        [('pending', 'Pending'),
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

    required_date = fields.Datetime(
        string='Required Date')

    supplier_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='purchase_req_partner',
        column1='partner_id',
        column2='supplier_id',
        string='Partner')

    @api.multi
    def change_state(self):
        self.state = 'in_process'
        if len(self.supplier_ids) == 1:
            purchase_order_obj = self.env['purchase.order']
            order_line = {
                'product_id': self.product_id.id,
                'name': self.name,
                'date_planned': self.required_date,
                'product_qty': self.product_qty,
                'product_uom': self.product_id.product_tmpl_id.uom_id.id,
                'price_unit': self.product_id.standard_price
            }
            purchase_order_obj.create({
                'partner_id': self.supplier_ids.id,
                'order_line': [(0, 0, order_line)]
            })
        if len(self.supplier_ids) > 1:
            requirement_obj = self.env['purchase.requirement']
            line_ids = {
                'product_id': self.product_id.id,
                'product_qty': self.product_qty,
                'schedule_date': self.required_date,
                'price_unit': self.product_id.standard_price
            }
            for partner in self.supplier_ids:
                requirement_obj.create({
                    'vendor_id': partner.id,
                    'ordering_date': self.required_date,
                    'line_ids': [(0, 0, line_ids)]
                })


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
