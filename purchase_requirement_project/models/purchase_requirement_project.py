# -*- coding: utf-8 -*-
from openerp import models, api, fields, _


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
