# -*- coding: utf-8 -*-
from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def action_rfq_send(self):
        result = super(PurchaseOrder, self).action_rfq_send()
        template_obj = self.env['mail.template']
        try:
            if self.env.context.get('send_rfq', False):
                template = template_obj.search(
                    [('name', '=', 'DTA - Solicitud de presupuesto')])
            else:
                template = template_obj.search(
                    [('name', '=', 'DTA - Pedido de compra')])
        except:
            template = False
        if template:
            template_id = template[0].id
            result['context'].update({
                'default_template_id': template_id,
            })
        return result
