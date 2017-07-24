# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class PurchaseRequirement(models.Model):
    _name = 'purchase.requirement'

    name = fields.Char(
        string='Description',
        required=True,
        readonly=True,
        states={'pending': [('readonly', False)],
                'reviwed': [('readonly', False)]})

    ref = fields.Char(
        string='Ref',
        readonly=True,
        states={'pending': [('readonly', False)],
                'reviwed': [('readonly', False)]})

    state = fields.Selection(
        [('pending', 'Pending'),
         ('reviwed', 'Reviwed'),
         ('in_process', 'In Process'),
         ('done', 'Done')],
        string='State',
        track_visibility='onchange',
        required=True,
        copy=False,
        readonly=True,
        default="pending")

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        readonly=True,
        states={'pending': [('readonly', False)],
                'reviwed': [('readonly', False)]})

    product_qty = fields.Float(
        string='Product Qty',
        readonly=True,
        states={'pending': [('readonly', False)],
                'reviwed': [('readonly', False)]})

    required_date = fields.Date(
        string='Required Date',
        required=True,
        readonly=True,
        states={'pending': [('readonly', False)],
                'reviwed': [('readonly', False)]})

    expected_date = fields.Date(
        string='Expected Date',
        compute='_compute_expected_date')

    supplier_ids = fields.Many2many(
        comodel_name='res.partner',
        relation='purchase_req_partner',
        column1='partner_id',
        column2='supplier_id',
        string='Partner',
        readonly=True,
        states={'pending': [('readonly', False)],
                'reviwed': [('readonly', False)]})

    purchase_order_line_ids = fields.One2many(
        comodel_name='purchase.order.line',
        inverse_name='purchase_requirement_id',
        string='Purchase Order Lines')

    @api.multi
    def set_reviewd(self):
        self.filtered(
            lambda r: r.state == 'pending').write({'state': 'reviwed'})

    @api.multi
    def set_done(self):
        self.filtered(
            lambda r: r.state == 'in_process').write({'state': 'done'})

    @api.multi
    def get_purchase_order_line_values(self):
        self.ensure_one()
        return {
            'product_id': self.product_id.id,
            'name': self.name,
            'date_planned': self.required_date,
            'required_date': self.required_date,
            'product_qty': self.product_qty,
            'product_uom':
                self.product_id.product_tmpl_id.uom_id.id,
            'price_unit': self.product_id.standard_price,
            'purchase_requirement_id': self.id,
        }

    @api.multi
    def generate_purchases(self):
        if self.filtered(
            lambda r: not r.supplier_ids and self.state == 'in_process'
        ):
            raise ValidationError(
                _("You must indicate at least one supplier to validate"))
        purchase_order_obj = self.env['purchase.order']
        orders_values = {}
        requirements = self.filtered(lambda r:
                                     r.supplier_ids and r.state == 'reviwed')
        requirements.write({'state': 'in_process'})
        for requirement in requirements:
            order_line = requirement.get_purchase_order_line_values()
            for partner in requirement.supplier_ids:
                if partner.id in orders_values.keys():
                    orders_values[partner.id].append((0, 0, order_line))
                else:
                    orders_values.update({
                        partner.id: [(0, 0, order_line)]
                    })
        for partner_id in orders_values.keys():
            purchase = purchase_order_obj.create({
                'partner_id': partner_id,
                'order_line': orders_values[partner_id]
            })
            purchase._auto_send_rfq()

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id.default_code:
            self.ref = self.product_id.default_code
        if self.product_id.seller_ids:
            self.update({
                'supplier_ids': [
                    (6, 0, self.product_id.seller_ids.mapped('name').ids)]
            })

    @api.multi
    def _compute_expected_date(self):
        for record in self:
            if record.state in ('pending', 'reviwed'):
                record.expected_date = record.required_date
            else:
                dates = record.purchase_order_line_ids.mapped('date_order')
                record.expected_date = dates and max(dates)
