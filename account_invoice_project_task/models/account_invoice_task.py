# -*- coding: utf-8 -*-

from openerp import models, api, fields, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Task')

    @api.multi
    def invoice_validate(self):
        result = 0
        if self.task_id.stage_id.name == 'done':
            self.task_id.stage_id.milestone_done = True
            import pdb
            pdb.set_trace()
        if not self.task_id.stage_id.milestone_done:
            raise Warning(
                _("The milestone must be in done before"))
        else:
            result = super(AccountInvoice, self).invoice_validate()
            import pdb
            pdb.set_trace()
        return result


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'

    milestone_done = fields.Boolean(
        string='Milestone')
