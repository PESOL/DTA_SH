# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class PartnerCustomer(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(
        string='Customer Code')

    @api.model
    def create(self, vals):
        if vals.get('customer'):
            vals.update({
                'customer_code': self.env[
                    'ir.sequence'].next_by_code('customer.code')
            })
        return super(PartnerCustomer, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('customer'):
            vals.update({
                'customer_code': self.env[
                    'ir.sequence'].next_by_code('customer.code')
            })
        return super(PartnerCustomer, self).write(vals)
