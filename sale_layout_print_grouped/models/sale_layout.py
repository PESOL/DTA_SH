# -*- coding: utf-8 -*-

from odoo import models, api, fields
from openerp.exceptions import ValidationError
from itertools import groupby


class SaleLayoutCategory(models.Model):
    _inherit = 'sale.layout_category'

    description = fields.Html(
        string='Description')

    print_grouped = fields.Boolean(
        string='Print Grouped')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def order_lines_layout(self):
        # report_pages = super(SaleLayoutCategory, self).order_lines_layouted()
        self.ensure_one()
        report_pages = [[]]
        for category, lines in groupby(self.order_line,
                                       lambda l: l.layout_category_id):
            # If last added category induced a pagebreak, this one will be on a
            # new page
            if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                report_pages.append([])
            # Append category to current report page
            report_pages[-1].append({
                'name': category and category.name or 'Uncategorized',
                'description': category and category.description,
                'print_grouped': category and category.print_grouped,
                'tax_id': self.order_line[0].tax_id,
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })
        return report_pages


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('tax_id')
    def _check_tax(self):
        lines = self.search([
            ('layout_category_id', '=', self.layout_category_id.id),
            ('order_id', '=', self.order_id.id)
        ]).filtered(lambda l: l.tax_id.id != self.tax_id.id)
        if len(lines) > 0:
            raise ValidationError(
                "the tax should be the same for the section")
