from odoo import models, fields, api, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_all_related_aml(self):
        return self.account_move_ids.line_ids

