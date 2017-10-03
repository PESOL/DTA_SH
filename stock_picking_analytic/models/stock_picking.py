# encoding: utf-8
from openerp import models, api, fields, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

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
        analytic_line_obj = self.env['account.analytic.line']
        for line in self.move_lines:
            if self.picking_type_id.analytic_type == 'out':
                amount = (line.product_id.lst_price *
                          line.product_uom_qty) * -1
            elif self.picking_type_id.analytic_type == 'in':
                amount = (line.product_id.lst_price *
                          line.product_uom_qty)
            else:
                amount = False
            if amount:
                analytic_line_obj.create({
                    'name': line.product_id.name,
                    'amount': amount,
                    'unit_amount': line.product_uom_qty,
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom.id,
                    'account_id': line.account_analytic_id.id
                })
        for line in self.move_lines:
            line.quant_ids.sudo().update({
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


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    analytic_type = fields.Selection(
        [('in', 'In'),
         ('out', 'Out'),
         ('no', 'No')],
        string='Analytic Type',
        default='no')
