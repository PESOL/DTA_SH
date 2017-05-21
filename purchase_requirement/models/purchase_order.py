# -*- coding: utf-8 -*-

from odoo import models, api, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_confirm(self):
        for line in self.mapped('order_line'):
            if line.purchase_requirement_id:
                line.purchase_requirement_id.purchase_order_line_ids.filtered(
                    lambda l: l.id != line.id
                ).unlink()
                line.purchase_requirement_id.set_done()

        return super(PurchaseOrder, self).button_confirm()

    @api.multi
    def _auto_send_rfq(self):
        @api.multi
        def action_rfq_send(self):
            self.ensure_one()
            template = self.env.ref('purchase.email_template_edi_purchase')
            ctx = dict(self.env.context or {})
            ctx.update({
                'default_model': 'purchase.order',
                'default_res_id': self.id,
                'default_use_template': bool(template.id),
                'default_template_id': template.id,
                'default_composition_mode': 'comment',
            })
            compose_obj = self.env['mail.compose.message']
            compose = compose_obj.with_context(ctx).create()
            compose.send_mail()
        # self.ensure_one()
        # Template = self.env['mail.template']
        # template_id = self.env.ref('purchase.email_template_edi_purchase')
        #
        # template = template_id.get_email_template(self.id)
        # body_html = Template.with_context(template._context).render_template(
        #     template.body_html, 'purchase.order', self.id)
        # subject_html = Template.with_context(
        #     template._context
        # ).render_template(template.subject, 'purchase.order', self.id)
        # self.message_post(
        #     body=body_html,
        #     subject=subject_html,
        #     partner_ids=self.partner_id.ids
        # )
        #
        # return True


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purchase_requirement_id = fields.Many2one(
        comodel_name='purchase.requirement',
        string='Purchase Requirement')
