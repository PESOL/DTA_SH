# -*- coding: utf-8 -*-

from odoo import models, api, fields


class SetSaleTemplate(models.TransientModel):
    _name = 'set.sale.template'

    template_id = fields.Many2one(
        comodel_name='sale.quote.template',
        string='Template')

    @api.multi
    def set_template(self):
        self.ensure_one()
        sale_id = self.env.context.get('active_id')
        sale = self.env['sale.order'].browse(sale_id)
        sale.update_template(self.template_id)
