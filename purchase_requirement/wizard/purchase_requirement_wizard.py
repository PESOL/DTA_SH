# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class PurchaseRequirementWizard(models.TransientModel):
    _name = 'purchase.requirement.wizard'

    requirement_ids = fields.Many2many(
        comodel_name='purchase.requirement',
        # default=_default_deposit_taxes_id,
        string='Requirements')
