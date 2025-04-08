from odoo import models, fields, api, _, tools
from datetime import datetime
from dateutil.relativedelta import relativedelta

class POSSubStock(models.Model):
    _name = 'pos.sub.stock'
    _description = 'POS Sub Stock'
    _rec_name = "sub_location_name"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    location_id = fields.Many2one("stock.location",'Main Location')
    sub_location_name = fields.Char('Location Name')
    product_family_ids = fields.Many2many('product.family','stock_product_family',string="Product Family")

    def action_show_stock_report(self):
        return {
                    'type': 'ir.actions.act_window',
                    'name': ('Stock Report'),
                    'res_model': 'product.stock.report',
                    'view_mode': 'tree',
                    'domain': [('product_family_id', 'in', self.product_family_ids.ids), ('location_id', '=', self.location_id.id)],
                    'context': {'search_default_group_by_product_id':1},
                }

class POSSubLocationReport(models.TransientModel):
    _name = 'pos.sub.report'
    _description = 'Product Move Report in POS by Sub Location'

    date = fields.Date("Date")
    sub_location_id = fields.Many2one('pos.sub.stock')

    def action_show_stock_report(self):
        start = datetime.combine(self.date, datetime.min.time())
        end = datetime.combine(self.date, datetime.max.time())
        return {
                'type': 'ir.actions.act_window',
                'name': ('POS Sub-Location Report at '+str(self.date) + ' for ' + str(self.sub_location_id.sub_location_name)),
                'res_model': 'product.stock.report',
                'view_mode': 'tree,form',
                'domain': [('product_family_id', 'in', self.sub_location_id.product_family_ids.ids), 
                            ('location_id', '=', self.sub_location_id.location_id.id),
                            ('date','>',start),('date','<',end)],
                'context': {'search_default_group_by_product_id':1},
                }

class ProductStockReport(models.Model):
    _name = 'product.stock.report'
    _description = 'Product Stock Report'
    _auto = False
    _rec_name = 'pos_reference'

    product_id = fields.Many2one('product.product', 'Product')
    default_code = fields.Char('Internal Reference')
    product_family_id = fields.Many2one('product.family','Product Family')
    product_group_id = fields.Many2one('product.group','Product Group')
    location_id = fields.Many2one('stock.location','Location')
    analytic_account_id = fields.Many2one('account.analytic.account','Analytic Account')
    pos_reference = fields.Char('Receipt Number')
    cashier_id = fields.Many2one('hr.employee','Cashier')
    session_id = fields.Many2one('pos.session','Session ID')

    quantity = fields.Float("Quantity")
    product_uom_id = fields.Many2one("uom.uom","UoM")
    price_unit = fields.Float("Unit Price")
    price_subtotal = fields.Float("Subtotal w/o Tax")
    date = fields.Datetime("Date")
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
            SELECT
                pos_line.id AS ID,
                pos.date_order As date,
                pos_line.product_id AS product_id,
                pos_line.qty As quantity,
                pos_line.price_unit As price_unit,
                pos_line.price_subtotal As price_subtotal,
                pt.default_code As default_code,
                pt.product_family_id As product_family_id,
                pt.product_group_id As product_group_id,
                pt.uom_id As product_uom_id,
                pos.analytic_account_id As analytic_account_id,
                pos.pos_reference As pos_reference,
                pos.employee_id As cashier_id,
                pos.session_id As session_id,
                picking_type.default_location_src_id As location_id
            FROM
                pos_order_line pos_line
                JOIN product_product pp ON pp.id = pos_line.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                JOIN pos_order pos ON pos.id = pos_line.order_id
                JOIN pos_session session ON session.id = pos.session_id
                JOIN pos_config config ON config.id = session.config_id
                JOIN stock_picking_type picking_type ON picking_type.id = config.picking_type_id
                """
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, query))
