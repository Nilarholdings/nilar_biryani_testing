from odoo import api, models, fields, _ 

class ProductProduct(models.Model):
    _inherit = 'product.product'

    onhand_qty = fields.Integer(string='Onhand Qty')
    is_check = fields.Boolean(string='Check?')


class PosConfig(models.Model):

    _inherit = 'pos.config'

    show_qty_available = fields.Boolean('Display Stock in POS', help="Apply show quantity of POS", default=True)
    location_only = fields.Boolean('Count only for POS Location', help='Only Show Stock Qty in this POS Location')
    allow_out_of_stock = fields.Boolean('Allow Out-of-Stock')
    limit_qty = fields.Integer('Deny Order When Available Qty Is Lower Than')
    hide_product = fields.Boolean('Hide Products which are not in POS Location',
                                  help='Hide products with negative stocks or not exist in the stock location of this POS')
    stock_location_id = fields.Many2one('stock.location', 'Stock Location', related='picking_type_id.default_location_src_id', store=True)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def check_on_hand_qty_batch(self, product_ids, config_id):
        # Assuming this method returns a list of quantities in the same order as product_ids
        quantities = []
        for product_id in product_ids:
            qty = self.env['product.product'].browse(product_id).with_context(
                location=config_id).qty_available
            quantities.append(qty)
        return quantities

