from openerp import models, api, fields, _


class ProjectBudget(models.Model):
    _name = 'project.budget'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project')

    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category')

    cost = fields.Float(
        string='Cost')

    imputed_amount = fields.Float(
        string='Imputed Amount')

    percent = fields.Float(
        string='Percent')


class Project(models.Model):
    _inherit = 'project.project'

    budget_ids = fields.One2many(
        comodel_name='project.budget',
        inverse_name='project_id',
        string='Project Budget')
