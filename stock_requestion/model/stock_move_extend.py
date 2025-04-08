from odoo import models, fields, api, _
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.misc import clean_context, OrderedSet
from odoo.exceptions import UserError
from collections import defaultdict


class StockMove(models.Model):
    _inherit = 'stock.move'
    requestion_type = fields.Selection([('issued', 'Issued'), ('received', 'Received')], string='Reqiestion Type')

    brand_id = fields.Many2one('product.brand', string='Brand',related='product_id.brand_id',store=True)
    remark = fields.Text(string='Remark')
    stock_req_id = fields.Many2one('stock.requestion.line', string='Stock Req')
    distribution_remark = fields.Char('Distribution Remark')

    def _action_done(self, cancel_backorder=False):
        res = super(StockMove, self)._action_done(cancel_backorder)
        for rec in self:
            if rec.requestion_type == 'issued':
                prev_qty = rec.stock_req_id.issued_qty
                if rec.location_id.usage == 'internal' and rec.location_dest_id.usage == 'transit':
                    sign = 1
                else:
                    sign = -1
                done_quantity = rec.quantity_done * sign
                rec.stock_req_id.issued_qty = done_quantity + prev_qty
            elif rec.requestion_type == 'received':
                prev_qty = rec.stock_req_id.received_qty
                if rec.location_id.usage == 'transit' and rec.location_dest_id.usage == 'internal':
                    sign = 1
                else:
                    sign = -1
                done_quantity = rec.quantity_done * sign
                rec.stock_req_id.received_qty = done_quantity + prev_qty
        return res