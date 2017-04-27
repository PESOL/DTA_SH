# -*- coding: utf-8 -*-

from odoo import models, api, fields, _


class ProjectBudget(models.Model):
    _name = 'project.budget'

    project_id = fields.Many2one(
        comodel_name='project.project',
        string='Project')

    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Product Category')

    budget = fields.Float(
        string='Budget')

    amount = fields.Float(
        string='Amount',
        compute='_compute_amount')

    percent = fields.Float(
        string='Percent',
        compute='_compute_amount')

    @api.multi
    def _compute_amount(self):
        product_category_obj = self.env['product.category']
        accon_obj = self.env['account.analytic.line']
        for budget in self:
            product_category_ids = product_category_obj.search([
                ('parent_left', '>=', budget.product_category_id.parent_left),
                ('parent_right', '<=', budget.product_category_id.parent_right)
            ]).ids
            amount = sum(accon_obj.search([
                ('account_id', '=', budget.project_id.analytic_account_id.id),
                ('product_category_id', 'in', product_category_ids),
            ]).mapped('amount'))
            budget.amount = amount
            budget.percent = (
                budget.budget > 0 and
                (budget.amount / budget.budget) * 100
            )or 0

    @api.multi
    def action_view_project_project(self):
        self.ensure_one()
        action = self.env.ref('project.open_view_project_all').read()[0]
        form_view_id = self.env.ref('project.edit_project').id

        action['views'] = [(form_view_id, 'form')]
        action['res_id'] = self.project_id.id
        action.pop('target', None)

        return action


class Project(models.Model):
    _inherit = 'project.project'

    budget_ids = fields.One2many(
        comodel_name='project.budget',
        inverse_name='project_id',
        string='Project Budget')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    project_budget = fields.Boolean(
        string='Project Budget')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()
        # line_obj = self.env['sale.order.line']
        # for line in line_obj.search([
        #     ('order_id.project_project_id', '!=', False),
        #     ('product_id.project_budget', '=', True)
        # ]):
        created_budget = {}
        project_budget_obj = self.env['project.budget']
        for line in self.filtered(
            'project_project_id'
        ).mapped('order_line').filtered('product_id.project_budget'):
            product_category_id = line.product_id.categ_id.id
            if product_category_id in created_budget.keys():
                budget = created_budget[product_category_id]
                budget.budget = (
                    line.product_uom_qty * line.price_unit + budget.budget)
            else:
                budget = project_budget_obj.create({
                    'project_id': line.order_id.project_id.id,
                    'product_category_id': product_category_id,
                    'budget': line.product_uom_qty * line.price_unit
                })
                created_budget.update({line.product_id.categ_id.id: budget})
        return result
