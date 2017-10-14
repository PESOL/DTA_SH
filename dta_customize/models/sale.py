# -*- coding: utf-8 -*-
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_quotation_send(self):
        result = super(SaleOrder, self).action_quotation_send()
        template_obj = self.env['mail.template']
        try:
            template = template_obj.search(
                    [('name', '=', 'DTA - Presupuesto venta')])
        except:
            template = False
        if template:
            template_id = template[0].id
            result['context'].update({
                'default_template_id': template_id,
            })
        return result

    @api.multi
    def get_access_action(self):
        self.ensure_one()
        return self[0].get_formview_action()
