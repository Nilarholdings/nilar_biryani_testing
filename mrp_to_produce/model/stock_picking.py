# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools, api, _


class TransferReport(models.Model):
    """ Stock Picking Analysis """

    _name = "stock.picking.report"
    _auto = False
    _description = "Stock Picking Analysis"
    _rec_name = 'id'

    name = fields.Char('Reference', readonly=True)
    scheduled_date = fields.Datetime('Scheduled Date', readonly=True)
    date_done = fields.Datetime('Effective Date', readonly=True)
    origin = fields.Char('Source Document', readonly=True)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', readonly=True)
    picking_type_code = fields.Selection([('incoming', 'Receipt'), ('outgoing', 'Delivery'), ('internal', 'Internal Transfer')],
                            'Type of Operation', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Contact', readonly=True)
    location_id = fields.Many2one('stock.location', "Source Location", readonly=True)
    location_dest_id = fields.Many2one('stock.location', "Destination Location", readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    brand_id = fields.Many2one('product.brand', 'Product Brand', readonly=True)
    product_family_id = fields.Many2one('product.family', 'Product Family', readonly=True)
    default_code = fields.Char('Internal Reference', readonly=True)
    description_bom_line = fields.Char('Kit', readonly=True)
    product_packaging_id = fields.Many2one('product.packaging', readonly=True)
    packaging_size = fields.Float('Packaging', readonly=True)
    multi_uom_qty = fields.Float('Demand', readonly=True)
    multi_qty_done = fields.Float('Done', readonly=True)
    multi_uom_line_id = fields.Many2one('multi.uom.line', 'Unit of Measure', readonly=True)
    remark = fields.Text('Remark', readonly=True)
    user_id = fields.Many2one('res.users', 'Responsible', readonly=True)
    received_by_id = fields.Many2one('hr.employee', 'Receive By', readonly=True)
    issued_by_id = fields.Many2one('hr.employee', 'Receive By', readonly=True)
    picking_id = fields.Many2one('stock.picking', 'Picking', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True)

    def _select(self):
        return """
            SELECT
                sm.id,
                sm.picking_id,
                sm.product_id,
                sm.product_packaging_id,
                sm.packaging_size,
                sm.multi_uom_qty,
                sml.multi_qty_done,
                sm.multi_uom_line_id,
                sm.remark,
                p.brand_id,
                p.product_family_id,
                p.default_code,
                sp.scheduled_date,
                sp.date_done,
                sp.origin,
                sp.name,
                sp.picking_type_id,
                sp.analytic_account_id,
                sp.partner_id,
                sp.location_id,
                sp.location_dest_id,
                sp.user_id,
                sp.state,
                sp.received_by_id,
                sp.issued_by_id
        """

    def _from(self):
        return """
            FROM stock_move sm
                left join stock_picking sp on (sp.id=sm.picking_id)
                join res_partner partner on sp.partner_id = partner.id
                    left join product_product p on (sm.product_id=p.id)
                    left join stock_move_line sml on (sm.id=sml.move_id)
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
               CREATE OR REPLACE VIEW %s AS (
                   %s
                   %s
               )
           """ % (self._table, self._select(), self._from())
                         )

