# -*- coding: utf-8 -*-

from openerp import models, api, fields, _
from openerp.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task')

    @api.multi
    def invoice_validate(self):
        res = {}
        if self.task_id.stage_id.name == 'done':
            self.task_id.stage_id.milestone_done = True
        if not self.task_id.stage_id.milestone_done:
            raise ValidationError(
                _("The milestone must be in the state 'done' before validate"))
        else:
            res = super(AccountInvoice, self).invoice_validate()
        return res


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    milestone_done = fields.Boolean(
        string='Milestone')
