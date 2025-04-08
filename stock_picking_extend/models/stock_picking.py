from odoo import models, fields, api, _

class Picking(models.Model):
    _inherit = "stock.picking"

    def update_product_qty(self):
        self.move_lines.convert_to_product_uom_qty()
        self.move_lines.convert_to_multi_uom_qty()