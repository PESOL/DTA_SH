# -*- coding: utf-8 -*-

from odoo import models, api, fields
from openerp.exceptions import ValidationError
from itertools import groupby


class AccountInvoiceLayoutCategory(models.Model):
    _name = 'account.invoice.layout_category'

    name = fields.Char(
        string='Name')
    sequence = fields.Integer(
        string='Sequence', required=True, default=10)
    subtotal = fields.Boolean(
        string='Add subtotal', default=True)
    pagebreak = fields.Boolean(
        string='Add pagebreak')
    description = fields.Html(
        string='Description')
    qty = fields.Float(
        string='Quantity')
    print_grouped = fields.Boolean(
        string='Print Grouped')
    quote_category_id = fields.Many2one(
        comodel_name='sale.layout_category',
        string='Template Section')
    account_invoice_id = fields.Many2one(
        comodel_name='account.invoice',
        string='Account Invoice')

    @api.onchange('quote_category_id')
    def onchange_quote_category_id(self):
        if self.quote_category_id:
            self.name = self.quote_category_id.name
            self.sequence = self.quote_category_id.sequence
            self.subtotal = self.quote_category_id.subtotal
            self.pagebreak = self.quote_category_id.pagebreak
            self.description = self.quote_category_id.description
            self.qty = self.quote_category_id.qty
            self.print_grouped = self.quote_category_id.print_grouped
            self.quote_category_id = self.quote_category_id.id


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    account_invoice_category_ids = fields.One2many(
        comodel_name='account.invoice.layout_category',
        inverse_name='account_invoice_id',
        string='Section')

    @api.multi
    def invoice_lines_layout(self):
        # report_pages = super(SaleLayoutCategory, self).order_lines_layouted()
        self.ensure_one()
        report_pages = [[]]
        for template_category, lines in groupby(
            self.invoice_line_ids,
                lambda l: l.layout_category_id):
            # If last added category induced a pagebreak, this one will be on a
            # new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            template_category_id = template_category.id
            category = self.account_invoice_category_ids.filtered(
                lambda c: c.quote_category_id.id == template_category_id
            ) or template_category
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'description': category and category.description,
                'category': category,
                'print_grouped': category and category.print_grouped,
                'tax_id': self.invoice_line_ids[0].invoice_line_tax_ids,
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })
        return report_pages

    @api.onchange('template_id')
    def onchange_template_id(self):
        super(AccountInvoice, self).onchange_template_id()
        template = self.template_id.with_context(lang=self.partner_id.lang)
        self.account_invoice_category_ids = []
        section_obj = [(2, 0,)]
        for layout_category in template.quote_layout_category_ids:
            data = {
                'name': layout_category.name,
                'subtotal': layout_category.subtotal,
                'print_grouped': layout_category.print_grouped,
                'sequence': layout_category.sequence,
                'qty': layout_category.qty,
                'pagebreak': layout_category.pagebreak,
                'description': layout_category.description,
                'quote_category_id': layout_category.id,
            }
            section_obj.append((0, 0, data))
        self.account_invoice_category_ids = section_obj


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.model
    def create(self, vals):
        invoice_id = vals.get('invoice_id')
        invoice = self.env['account.invoice'].browse(invoice_id)
        layout_category_id = vals.get('layout_category_id')
        layout_category = self.env['sale.layout_category'].browse(
            layout_category_id)
        invoice_layout_category_ids =  \
            invoice.account_invoice_category_ids.mapped('quote_category_id')
        if layout_category not in invoice_layout_category_ids:
            data = {
                'name': layout_category.name,
                'subtotal': layout_category.subtotal,
                'print_grouped': layout_category.print_grouped,
                'sequence': layout_category.sequence,
                'qty': layout_category.qty,
                'pagebreak': layout_category.pagebreak,
                'description': layout_category.description,
                'quote_category_id': layout_category.id,
            }
            invoice.update({
                'account_invoice_category_ids': [(0, 0, data)]
            })
        return super(AccountInvoiceLine, self).create(vals)

    @api.constrains('invoice_line_tax_ids')
    def _check_tax(self):
        lines = self.search([
            ('layout_category_id', '=', self.layout_category_id.id),
            ('invoice_id', '=', self.invoice_id.id)
        ]).filtered(
            lambda l: l.invoice_line_tax_ids.id != self.invoice_line_tax_ids.id
        )
        if len(lines) > 0:
            raise ValidationError(
                "the tax should be the same for the section")
