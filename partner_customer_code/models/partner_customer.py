# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class PartnerCustomer(models.Model):
    _inherit = 'res.partner'

    partner_customer_code = fields.Char(
        string='Customer Code')

    @api.model
    def create(self, vals):
        if vals.get('customer'):
            vals.update({
                'partner_customer_code': self.env[
                    'ir.sequence'].next_by_code('partner.customer.code')
            })
        return super(PartnerCustomer, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('customer') and vals.get('partner_customer_code') is False:
            vals.update({
                'partner_customer_code': self.env[
                    'ir.sequence'].next_by_code('partner.customer.code')
            })
        return super(PartnerCustomer, self).write(vals)
