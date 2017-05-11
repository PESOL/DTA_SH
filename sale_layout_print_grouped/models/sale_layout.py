# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from openerp.exceptions import ValidationError
from itertools import groupby

from datetime import datetime, timedelta

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
    def onchange_template_id(self):
        if not self.template_id:
            return
        template = self.template_id.with_context(lang=self.partner_id.lang)
        category_obj = self.env['sale.layout_category']
        self.sale_layout_category_ids = []
        category_ids = []
        category_rel = {}
        for layout_category in template.quote_layout_category_ids:
            new_category = category_obj.create({
                'name': layout_category.name + ' bis',
                'subtotal': layout_category.subtotal,
                'print_grouped': layout_category.print_grouped,
                'sequence': layout_category.sequence,
                'qty': layout_category.qty,
                'pagebreak': layout_category.pagebreak,
                'description': layout_category.description,
                'quote_category_id': layout_category.id,
            })
            category_ids.append(new_category.id)
            category_rel.update({layout_category.id: new_category.id})

        self.sale_layout_category_ids = [(6, 0, category_ids)]

        order_lines = [(5, 0, 0)]
        for line in template.quote_line:
            if self.pricelist_id:
                price = self.pricelist_id.with_context(
                    uom=line.product_uom_id.id).get_product_price(
                        line.product_id, 1, False)
            else:
                price = line.price_unit

            data = {
                'name': line.name,
                'price_unit': price,
                'discount': line.discount,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'layout_category_id': category_rel[line.layout_category_id.id],
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
                'customer_lead': self._get_customer_lead(
                    line.product_id.product_tmpl_id),
            }
            if self.pricelist_id:
                data.update(self.env['sale.order.line']._get_purchase_price(
                    self.pricelist_id, line.product_id, line.product_uom_id, fields.Date.context_today(self)))
            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = []
        for option in template.options:
            if self.pricelist_id:
                price = self.pricelist_id.with_context(
                    uom=option.uom_id.id).get_product_price(option.product_id, 1, False)
            else:
                price = option.price_unit
            data = {
                'product_id': option.product_id.id,
                'layout_category_id': option.layout_category_id,
                'name': option.name,
                'quantity': option.quantity,
                'uom_id': option.uom_id.id,
                'price_unit': price,
                'discount': option.discount,
                'website_description': option.website_description,
            }
            option_lines.append((0, 0, data))
        self.options = option_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.to_string(
                datetime.now() + timedelta(template.number_of_days))

        self.website_description = template.website_description
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note

    # @api.onchange('template_id')
    # def onchange_template_id(self):
    #     super(SaleOrder, self).onchange_template_id()
    #     template = self.template_id.with_context(lang=self.partner_id.lang)
    #     self.sale_layout_category_ids = []
    #     section_obj = [(2, 0,)]
    #     for layout_category in template.quote_layout_category_ids:
    #         data = {
    #             'name': layout_category.name + ' bis',
    #             'subtotal': layout_category.subtotal,
    #             'print_grouped': layout_category.print_grouped,
    #             'sequence': layout_category.sequence,
    #             'qty': layout_category.qty,
    #             'pagebreak': layout_category.pagebreak,
    #             'description': layout_category.description,
    #             'quote_category_id': layout_category.id,
    #         }
    #         section_obj.append((0, 0, data))
    #     self.sale_layout_category_ids = section_obj
    #
    #     for line in self.order_line:
    #         layout_category_id = line.layout_category_id.id
    #         line.layout_category_id = self.sale_layout_category_ids.filtered(
    #             lambda c: c.quote_category_id.id == layout_category_id
    #         )

    # @api.multi
    # def set_template(self):
    #     self.ensure_one()
    #     template = self.template_id.with_context(lang=self.partner_id.lang)
    #     section_rel = {}
    #     self.order_line = [(2, 0)]
    #     self.sale_layout_category_ids = [(2, 0)]
    #     sale_order_line_obj = self.order_line
    #     for section in template.quote_layout_category_ids:
    #         new_section = section.copy(
    #             {'quote_id': False, 'sale_order_id': self.id})
    #         section_rel.update({section.id: new_section.id})
    #     for line in template.quote_line:
    #         vals = {
    #             'layout_category_id': line.layout_category_id.id,
    #             'order_id': self.id,
    #             'product_id': line.product_id.id,
    #             'name': line.name,
    #             'product_uom_qty': line.product_uom_qty,
    #             'product_uom': line.product_uom_id.id,
    #             'price_unit': line.price_unit,
    #             'purchase_price':
    #                 line.product_id.product_tmpl_id.standard_price,
    #             'tax_id': line.product_id.product_tmpl_id.taxes_id,
    #             'price_subtotal': line.price_unit * line.product_uom_qty,
    #             'quote_id': line.quote_id
    #         }
    #         sale_order_line_obj.create(vals)
    #
    #     return {
    #         'type': 'ir.actions.client',
    #         'tag': 'reload',
    #     }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.constrains('tax_id')
    def _check_tax(self):
        lines = self.search([
            ('layout_category_id', '=', self.layout_category_id.id),
            ('order_id', '=', self.order_id.id),
            ('layout_category_id.print_grouped', '=', True)
        ]).filtered(lambda l: l.tax_id.id != self.tax_id.id)
        if len(lines) > 0:
            raise ValidationError(
                _("the tax should be the same for the section"))


class SaleQuoteTemplate(models.Model):
    _inherit = 'sale.quote.template'

    quote_layout_category_ids = fields.One2many(
        comodel_name='sale.layout_category',
        inverse_name='quote_id',
        string='Section')
