# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class SaleInvoicingMethod(models.Model):
    _name = 'sale.invoicing.method'

    name = fields.Char(
        string='Name',
        translate=True)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    invoicing_method_id = fields.Many2one(
        comodel_name='sale.invoicing.method',
        string='Invocing Method')
