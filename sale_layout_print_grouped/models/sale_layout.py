# -*- coding: utf-8 -*-

from odoo import models, api, fields
from openerp.exceptions import ValidationError
from itertools import groupby


class SaleLayoutCategory(models.Model):
    _inherit = 'sale.layout_category'

    description = fields.Html(
        string='Description')

    qty = fields.Float(
        string='Quantity')

    print_grouped = fields.Boolean(
        string='Print Grouped')

    quote_id = fields.Many2one(
        comodel_name='sale.quote.template',
        string='Quote Line')


class SaleOrderLayoutCategory(models.Model):
    _name = 'sale.order.layout_category'

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
    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order')

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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_layout_category_ids = fields.One2many(
        comodel_name='sale.order.layout_category',
        inverse_name='sale_order_id',
        string='Section')

    @api.multi
    def order_lines_layout(self):
        # report_pages = super(SaleLayoutCategory, self).order_lines_layouted()
        self.ensure_one()
        report_pages = [[]]
        for template_category, lines in groupby(
            self.order_line,
                lambda l: l.layout_category_id):
            # If last added category induced a pagebreak, this one will be on a
            # new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            template_category_id = template_category.id
            category = self.sale_layout_category_ids.filtered(
                lambda c: c.quote_category_id.id == template_category_id
            ) or template_category
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'description': category and category.description,
                'category': category,
                'print_grouped': category and category.print_grouped,
                'tax_id': self.order_line[0].tax_id,
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })
        return report_pages

    @api.onchange('template_id')
    def onchange_template_id(self):
        super(SaleOrder, self).onchange_template_id()
        template = self.template_id.with_context(lang=self.partner_id.lang)
        self.sale_layout_category_ids = []
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
        self.sale_layout_category_ids = section_obj


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('tax_id')
    def _check_tax(self):
        lines = self.search([
            ('order_id.sale_layout_category_ids', '!=', False),
            ('layout_category_id', '=', self.layout_category_id.id),
            ('order_id', '=', self.order_id.id)
        ]).filtered(lambda l: l.tax_id.id != self.tax_id.id)
        if len(lines) > 0 and self.tax_id:
            raise ValidationError(
                "the tax should be the same for the section")


class SaleQuoteTemplate(models.Model):
    _inherit = 'sale.quote.template'

    quote_layout_category_ids = fields.One2many(
        comodel_name='sale.layout_category',
        inverse_name='quote_id',
        string='Section')
