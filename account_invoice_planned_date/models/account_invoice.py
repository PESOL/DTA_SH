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

    client_ref = fields.Char(
        string='Client Reference',
        compute='_compute_search_client_ref')

    @api.multi
    def _compute_search_client_ref(self):
        sale_order_obj = self.env['sale.order'].search([
            ('name', '=', self.origin)
        ])
        if sale_order_obj.client_order_ref and len(sale_order_obj) == 1:
            self.client_ref = sale_order_obj.client_order_ref
        elif len(sale_order_obj) > 1:
            self.client_ref = sale_order_obj[0].client_order_ref
