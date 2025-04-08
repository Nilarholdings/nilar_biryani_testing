from odoo import models, fields, _
from collections import defaultdict


class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    account_move_line_id = fields.Many2one('account.move.line', 'Invoice Line', readonly=True, check_company=True, index="btree_not_null")
    price_diff_value = fields.Float('Invoice value correction with invoice currency')

    def _get_layer_price_unit(self):
        """ This function returns the value of product in a layer per unit, relative to the aml
            the function is designed to be overriden to add logic to price unit calculation
        :param layer: the layer the price unit is derived from
        """
        return self.value / self.quantity

    def _validate_accounting_entries(self):
        am_vals = []
        aml_to_reconcile = defaultdict(set)
        for svl in self:
            if not svl.with_company(svl.company_id).product_id.valuation == 'real_time':
                continue
            if svl.currency_id.is_zero(svl.value):
                continue
            move = svl.stock_move_id
            if not move:
                move = svl.stock_valuation_layer_id.stock_move_id
            am_vals += move.with_company(svl.company_id)._account_entry_move(svl.quantity, svl.description, svl.id,
                                                                             svl.value)
        if am_vals:
            account_moves = self.env['account.move'].sudo().create(am_vals)
            account_moves._post()
        for svl in self:
            move = svl.stock_move_id
            product = svl.product_id
            if svl.company_id.anglo_saxon_accounting:
                move._get_related_invoices()._stock_account_anglo_saxon_reconcile_valuation(product=product)
            for aml in (move | move.origin_returned_move_id)._get_all_related_aml():
                if aml.reconciled or aml.move_id.state != "posted" or not aml.account_id.reconcile:
                    continue
                aml_to_reconcile[(product, aml.account_id)].add(aml.id)
        for aml_ids in aml_to_reconcile.values():
            self.env['account.move.line'].browse(aml_ids).reconcile()

