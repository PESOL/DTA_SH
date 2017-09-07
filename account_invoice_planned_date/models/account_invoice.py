# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    planned_date = fields.Date(
        string='Planned Date',
        required=False)

    your_reference = fields.Char(
        string='Your Reference')

    suppl_code = fields.Char(
        string='Supplier code')
