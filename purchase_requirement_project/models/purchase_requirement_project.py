# -*- coding: utf-8 -*-
from openerp import models, api, fields


class PurchaseRequirementProject(models.Model):
    _name = 'purchase.requirement.project'

    name = fields.Char(
        string='Name')

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project')


class Project(models.Model):
    _inherit = 'project.project'

    purchase_requirement_ids = fields.One2many(
        comodel_name='purchase.requirement.project',
        inverse_name='project_id',
        string='Purchase Requirement Project')


class PurchaseRequirement(models.Model):
    _inherit = 'purchase.requirement'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project')

    @api.multi
    def get_purchase_order_line_values(self):
        values = super(PurchaseRequirement,
                       self).get_purchase_order_line_values()
        values.update({
            'account_analytic_id': self.project_id.analytic_account_id.id
        })
        return values
