# -*- coding: utf-8 -*-
# Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class ProjectProject(models.Model):
    _inherit = "project.project"

    document_page_id = fields.Many2one(
        string='Document Page',
        comodel_name='document.page',
    )
    
    