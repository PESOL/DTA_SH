# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task')

    task_done = fields.Boolean(
        string='Task Done',
        compute='_compute_task_done')

    @api.depends('task_id')
    def _compute_task_done(self):
        if self.task_id.stage_id.milestone_done:
            self.task_done = True

    @api.multi
    def invoice_validate(self):
        res = {}
        if self.task_id.stage_id.closed:
            self.task_id.stage_id.milestone_done = True
        if not self.task_id.stage_id.milestone_done and self.task_id:
            raise ValidationError(
                _("The milestone must be in the state 'done' before validate"))
        else:
            res = super(AccountInvoice, self).invoice_validate()
        return res


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    milestone_done = fields.Boolean(
        string='Milestone')
