from odoo import models, fields, api, _, tools
from datetime import datetime
from dateutil.relativedelta import relativedelta

class StockReceivedReport(models.Model):
    _name = 'stock.received.report'
    _description = 'Stock Received Report'
    _auto = False
    _rec_name = 'picking_number'

    partner_id = fields.Many2one('res.partner','Contact')
    product_id = fields.Many2one('product.product','Product')
    multi_uom_qty = fields.Float('Demand')
    multi_quantity_done = fields.Float('Done')
    picking_number = fields.Char("Reference")
    origin = fields.Char("Source Document")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status')
    scheduled_date = fields.Datetime('Scheduled Date')
    date = fields.Datetime('Created Date')
    multi_uom_line_id = fields.Many2one('multi.uom.line', 'UOM')
    remark = fields.Text("Remark")
    product_packaging_id = fields.Many2one('product.packaging','Packaging Size')
    packaging_size = fields.Float("Packaging")
    analytic_account_id = fields.Many2one('account.analytic.account','Analytic Account')
    # employee_id = fields.Many2one('hr.employee','Employee')

    backorder_id = fields.Many2one('stock.picking', 'Back Order of')

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
            SELECT
                sm.id AS id,
                sm.product_id As product_id,
                sm.multi_uom_qty As multi_uom_qty,
                sm.difference_quantity As multi_quantity_done,
                COALESCE(sm.multi_uom_line_id, 0) AS multi_uom_line_id,
                sp.name As picking_number,
                sp.origin As origin,
                sp.state As state,
                sp.scheduled_date As scheduled_date,
                sp.date As date,
                COALESCE(sm.product_packaging_id, 0) AS product_packaging_id,
                COALESCE(sm.packaging_size, 0) AS packaging_size,
               
                sm.remark As remark,
                COALESCE(sp.partner_id, 0) AS partner_id,
                COALESCE(sp.analytic_account_id, 0) AS analytic_account_id,
                COALESCE(sp.backorder_id, 0) AS backorder_id
            FROM
                stock_move sm
                JOIN stock_picking sp ON sp.id = sm.picking_id
            WHERE
                sm.multi_uom_qty != sm.difference_quantity
                AND sp.state in ('done','cancel')
                """
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, query))
