# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class ParterCustomer(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(
        string='Customer Code')


class SaleOrder(models.Model):
    _inherit = 'sale.order'
