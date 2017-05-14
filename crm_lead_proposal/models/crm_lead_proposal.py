# -*- encoding: utf-8 -*-
from openerp import models, api, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    proposal_ids = fields.One2many(
        comodel_name='crm.lead.proposal',
        inverse_name='crm_lead_id',
        string='Proposals')


class CrmLeadProposal(models.Model):
    _name = 'crm.lead.proposal'

    name = fields.Char(
        string='name')
    date = fields.Date(
        string='Date')
    template = fields.Boolean(
        string='Template',
        default=False)
    crm_lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead')
    template_id = fields.Many2one(
        comodel_name='crm.lead.proposal',
        string='Template')
    proposal_section_ids = fields.One2many(
        comodel_name='crm.lead.proposal.section',
        inverse_name='crm_lead_proposal_id',
        string='Sections')
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner')

    @api.multi
    def get_sections_values(self):
        self.ensure_one()
        sections_values = []
        for section in self.proposal_section_ids:
            sections_values.append([0, 0, {
                'name': section.name,
                'sequence': section.sequence,
                'crm_proposal_page_ids': section.get_pages_values(),
            }])
        return sections_values

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.name = self.template_id.name
            self.proposal_section_ids = self.template_id.get_sections_values()


class CrmLeadProposalSection(models.Model):
    _name = 'crm.lead.proposal.section'
    _order = 'sequence'
    name = fields.Char(
        string='Name')
    sequence = fields.Integer(
        string='Sequence')
    template_id = fields.Many2one(
        comodel_name='crm.lead.proposal.section',
        string='Template')
    crm_lead_proposal_id = fields.Many2one(
        comodel_name='crm.lead.proposal',
        string='Lead Proposal')
    crm_proposal_page_ids = fields.One2many(
        comodel_name='crm.lead.proposal.page',
        inverse_name='crm_proposal_section_id',
        string='Pages')
    template = fields.Boolean(
        string='Template',
        default=False)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        related='crm_lead_proposal_id.partner_id')

    @api.multi
    def get_pages_values(self):
        self.ensure_one()
        pages_values = []
        for page in self.crm_proposal_page_ids:
            pages_values.append([0, 0, {
                'name': page.name,
                'sequence': page.sequence,
                'description': page.description,
            }])
        return pages_values

    @api.onchange('template_id')
    def _onchange_template_id(self):
        if self.template_id:
            self.name = self.template_id.name
            self.sequence = self.template_id.sequence
            self.crm_proposal_page_ids = self.template_id.get_pages_values()


class CrmLeadProposalPage(models.Model):
    _name = 'crm.lead.proposal.page'
    _order = 'sequence'

    name = fields.Char(
        string='Name')
    sequence = fields.Integer(
        string='Sequence')
    crm_proposal_section_id = fields.Many2one(
        comodel_name='crm.lead.proposal.section',
        string='Section')
    description = fields.Html(
        string='Description')
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Partner',
        related='crm_proposal_section_id.crm_lead_proposal_id.partner_id')
