# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_supplier_code = fields.Char(
        string='Supplier Customer Code')

    @api.model
    def create(self, vals):
        if vals.get('supplier'):
            vals.update({
                'partner_supplier_code': self.env[
                    'ir.sequence'].next_by_code('supplier.customer.code')
            })
        return super(ResPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('supplier') and vals.get('partner_supplier_code')\
                is False:
            vals.update({
                'partner_supplier_code': self.env[
                    'ir.sequence'].next_by_code('supplier.customer.code')
            })
        return super(ResPartner, self).write(vals)
