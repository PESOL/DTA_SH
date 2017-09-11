# -*- coding: utf-8 -*-

from odoo import models, api, fields
from openerp.exceptions import ValidationError
from itertools import groupby

from datetime import datetime, timedelta

import odoo.addons.decimal_precision as dp


class SaleLayoutCategory(models.Model):
    _inherit = 'sale.layout_category'

    description = fields.Html(
        string='Description')

    qty = fields.Float(
        string='Quantity',
        digits=dp.get_precision('Quantity'))

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
        string='Quantity',
        digits=dp.get_precision('Quantity'))
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

    # @api.onchange('template_id')
    # def onchange_template_id(self):
    #     super(SaleOrder, self).onchange_template_id()
    #     template = self.template_id.with_context(lang=self.partner_id.lang)
    #     self.sale_layout_category_ids = []
    #     section_obj = [(2, 0,)]
    #     for layout_category in template.quote_layout_category_ids:
    #         data = {
    #             'name': layout_category.name,
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

    @api.multi
    def update_template(self, template_id):
        self.ensure_one()
        if not template_id:
            return
        self.template_id = template_id
        template = self.template_id.with_context(lang=self.partner_id.lang)

        order_lines = [(5, 0, 0)]
        for line in template.quote_line:
            if self.pricelist_id:
                price = self.pricelist_id.with_context(
                    uom=line.product_uom_id.id
                ).get_product_price(line.product_id, 1, False)
            else:
                price = line.price_unit

            data = {
                'name': line.name,
                'price_unit': price,
                'discount': line.discount,
                'product_uom_qty': line.product_uom_qty,
                'product_id': line.product_id.id,
                'layout_category_id': line.layout_category_id,
                'product_uom': line.product_uom_id.id,
                'website_description': line.website_description,
                'state': 'draft',
                'customer_lead': self._get_customer_lead(
                    line.product_id.product_tmpl_id),
            }
            if self.pricelist_id:
                data.update(self.env['sale.order.line']._get_purchase_price(
                    self.pricelist_id, line.product_id, line.product_uom_id,
                    fields.Date.context_today(self)))
            order_lines.append((0, 0, data))

        self.order_line = order_lines
        self.order_line._compute_tax_id()

        option_lines = [(5, 0, 0)]
        for option in template.options:
            if self.pricelist_id:
                price = self.pricelist_id.with_context(
                    uom=option.uom_id.id
                ).get_product_price(option.product_id, 1, False)
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

        self.sale_layout_category_ids = [(5, 0, 0)]
        section_lines = []
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
            section_lines.append((0, 0, data))
        self.sale_layout_category_ids = section_lines

        if template.number_of_days > 0:
            self.validity_date = fields.Date.to_string(
                datetime.now() + timedelta(template.number_of_days))

        self.website_description = template.website_description
        self.require_payment = template.require_payment

        if template.note:
            self.note = template.note

    @api.multi
    def set_template(self):
        action_name = 'set_sale_template_action'
        ir_model_obj = self.env['ir.model.data']
        model, action_id = ir_model_obj.get_object_reference(
            'sale_layout_print_grouped', action_name)
        [action] = self.env[model].browse(action_id).read()
        return action


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
