# encoding: utf-8
from openerp import models, api, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Account Analytic')

    @api.multi
    def do_new_transfer(self):
        if self.account_analytic_id:
            account_analytic_obj = self.env['account.analytic.account']
            analytic_line_obj = self.env['account.analytic.line']
            # amount = 0
            vals = []
            for product in self.move_lines:
                # amount += (product.price_unit * product.product_uom_qty) * -1
                data = analytic_line_obj.create({
                    'name': self.partner_id.name,
                    'amount': product.product_id.lst_price,
                    'product_id': product.product_id.id,
                    'product_uom_id': product.product_uom.id,
                    'account_id': self.account_analytic_id.id
                })
                vals.append(data)
            # import pdb
            # pdb.set_trace()
            account_analytic_obj.create({
                'name': self.partner_id.name,
                'account_id': self.account_analytic_id.id,
                'partner_id': self.partner_id.id,
                'company_id': self.company_id.id,
                'line_ids': vals
            })
        return super(StockPicking, self).do_new_transfer()
