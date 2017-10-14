# -*- coding: utf-8 -*-

from odoo import models, api, fields


class ProjectForecast(models.Model):
    _inherit = 'project.forecast'

    estimated_hours = fields.Float(
        string='Estimated Hours',
        related='task_id.planned_hours')

    limit_date = fields.Date(
        string='Limit Date',
        related='task_id.date_deadline')

    imputed_hours = fields.Float(
        string='Real Imputed Hours',
        related='task_id.effective_hours')
