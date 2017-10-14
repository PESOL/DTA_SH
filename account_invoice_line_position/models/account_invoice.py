# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    position = fields.Char(
        string='Position')
