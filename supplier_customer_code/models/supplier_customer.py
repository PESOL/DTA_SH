# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class SupplierCustomer(models.Model):
    _inherit = 'res.partner'

    supplier_customer_code = fields.Char(
        string='Supplier Customer Code')

    @api.model
    def create(self, vals):
        if vals.get('supplier'):
            vals.update({
                'supplier_customer_code': self.env[
                    'ir.sequence'].next_by_code('supplier.customer.code')
            })
        return super(SupplierCustomer, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('supplier') and vals.get('supplier_customer_code')\
                is False:
            vals.update({
                'supplier_customer_code': self.env[
                    'ir.sequence'].next_by_code('supplier.customer.code')
            })
        return super(SupplierCustomer, self).write(vals)
