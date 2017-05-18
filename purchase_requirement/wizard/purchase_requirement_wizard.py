# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class PurchaseRequirementWizard(models.TransientModel):
    _name = 'purchase.requirement.wizard'

    requirement_ids = fields.Many2many(
        comodel_name='purchase.requirement',
        default=lambda self: self._context.get('active_ids'),
        string='Requirements')

    @api.multi
    def default_requirement_active_id(self):
        result = self.requirement_ids.generate_sales
        return result
