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

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order')

    quote_id = fields.Many2one(
        comodel_name='sale.quote.template',
        string='Quote Line')
    quote_category_id = fields.Many2one(
        comodel_name='sale.layout_category',
        string='Template Section')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_layout_category_ids = fields.One2many(
        comodel_name='sale.layout_category',
        inverse_name='sale_order_id',
        string='Section')

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
                'category': category,
                'print_grouped': category and category.print_grouped,
                'tax_id': self.order_line[0].tax_id,
                'subtotal': category and category.subtotal,
                'pagebreak': category and category.pagebreak,
                'lines': list(lines)
            })
        return report_pages

    @api.onchange('template_id')
    def _onchange_template_id(self):
        pass
        # super(SaleOrder, self).onchange_template_id()
        # template = self.template_id.with_context(lang=self.partner_id.lang)
        # self.sale_layout_category_ids = []
        # section_obj = [(2, 0,)]
        # for line in template.quote_line:
        #     data = {
        #         'name': line.layout_category_id.name,
        #         'subtotal': line.layout_category_id.subtotal,
        #         'print_grouped': line.layout_category_id.print_grouped,
        #         'sequence': line.layout_category_id.sequence,
        #         'qty': line.layout_category_id.qty,
        #         'pagebreak': line.layout_category_id.pagebreak,
        #         'description': line.layout_category_id.description,
        #         'quote_category_id': line.layout_category_id.id,
        #     }
        #     section_obj.append((0, 0, data))
        # self.sale_layout_category_ids = section_obj
        #
        # for line in self.order_line:
        #     layout_category_id = line.layout_category_id.id
        #     line.layout_category_id = self.sale_layout_category_ids.filtered(
        #         lambda c: c.quote_category_id.id == layout_category_id
        #     )[0]

    @api.multi
    def set_template(self):
        self.ensure_one()
        template = self.template_id.with_context(lang=self.partner_id.lang)
        section_rel = {}
        self.order_line = [(2, self.id)]
        self.sale_layout_category_ids = [(2, 0)]
        sale_order_line_obj = self.order_line
        for section in template.quote_layout_category_ids:
            new_section = section.copy(
                {'quote_id': False, 'sale_order_id': self.id})
            section_rel.update({section.id: new_section.id})
        for line in template.quote_line:
            vals = {
                'layout_category_id': line.layout_category_id.id,
                'order_id': self.id,
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom_id.id,
                'price_unit': line.price_unit,
                'purchase_price':
                    line.product_id.product_tmpl_id.standard_price,
                'tax_id': line.product_id.product_tmpl_id.taxes_id,
                'price_subtotal': line.price_unit * line.product_uom_qty,
                'quote_id': line.quote_id
            }
            sale_order_line_obj.create(vals)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }


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


class SaleQuoteTemplate(models.Model):
    _inherit = 'sale.quote.template'

    quote_layout_category_ids = fields.One2many(
        comodel_name='sale.layout_category',
        inverse_name='quote_id',
        string='Section')
