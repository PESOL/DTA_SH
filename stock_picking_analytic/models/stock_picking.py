# encoding: utf-8
from openerp import models, api, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Account Analytic')

    @api.multi
    def do_new_transfer(self):
        # self.action_confirm()
        # self.action_assign()
        # for pack in self.pack_operation_product_ids:
        #     if pack.product_qty > 0:
        #         pack.write({'qty_done': pack.product_qty})
        #     else:
        #         pack.unlink()
        result = super(StockPicking, self).do_new_transfer()
        if self.account_analytic_id:
            analytic_line_obj = self.env['account.analytic.line']
            for line in self.move_lines:
                amount = sum(
                    [q.location_id == line.location_dest_id and
                     q.inventory_value for q in line.quant_ids]) * -1
                analytic_line = analytic_line_obj.create({
                    'name': self.partner_id.name,
                    'amount': amount,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'account_id': self.account_analytic_id.id
                })
        for line in self.move_lines:
            line.quant_ids.update({
                'account_analytic_id': line.account_analytic_id.id
            })
        return result


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def _create_picking(self):
        result = super(PurchaseOrder, self)._create_picking()
        for line in self.order_line:
            line.move_ids.update({
                'account_analytic_id': line.account_analytic_id.id
            })
        return result


class StockMove(models.Model):
    _inherit = 'stock.move'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Account Analytic')


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Account Analytic')
