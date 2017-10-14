# -*- coding: utf-8 -*-

from openerp import models, api, fields


class PurchaseRequirementWizard(models.TransientModel):
    _name = 'purchase.requirement.wizard'

    requirement_ids = fields.Many2many(
        comodel_name='purchase.requirement',
        default=lambda self: self._context.get('active_ids'),
        string='Requirements')

    @api.multi
    def generate_purchases(self):
        return self.requirement_ids.generate_purchases()


class PurchaseRequirementSetOk(models.TransientModel):
    _name = 'purchase.requirement.set.ok'

    requirement_ids = fields.Many2many(
        comodel_name='purchase.requirement',
        default=lambda self: self._context.get('active_ids'),
        string='Requirements')

    @api.multi
    def set_reviewd(self):
        return self.requirement_ids.set_reviewd()
