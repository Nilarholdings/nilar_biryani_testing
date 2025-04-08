from odoo import api, models, fields, _
from odoo.exceptions import UserError

class StockMove(models.Model):

    _inherit = 'stock.move'

    multi_scrap_analytic_acc_id = fields.Many2one('account.analytic.account', 'Multi Scrap Analytic Account')
    analytic_tag_ids = fields.Many2many('account.analytic.tag',string="Analytic Tags")

    def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id, cost):
        values = super(StockMove, self)._prepare_account_move_vals(credit_account_id,
                                                                   debit_account_id,
                                                                   journal_id,
                                                                   qty,
                                                                   description,
                                                                   svl_id,
                                                                   cost)
        values.update({'analytic_account_id': self.multi_scrap_analytic_acc_id.id,'analytic_tag_ids': self.analytic_tag_ids})
        return values

    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description):
        res = super(StockMove, self)._generate_valuation_lines_data(partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id, description)
        debit_line_vals = {
            'name': description,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'debit': debit_value if debit_value > 0 else 0,
            'credit': -debit_value if debit_value < 0 else 0,
            'account_id': debit_account_id,
            'analytic_tag_ids': self.analytic_tag_ids,
        }

        credit_line_vals = {
            'name': description,
            'product_id': self.product_id.id,
            'quantity': qty,
            'product_uom_id': self.product_id.uom_id.id,
            'ref': description,
            'partner_id': partner_id,
            'credit': credit_value if credit_value > 0 else 0,
            'debit': -credit_value if credit_value < 0 else 0,
            'account_id': credit_account_id,
            'analytic_tag_ids' : self.analytic_tag_ids,
        }
        res.update({'credit_line_vals': credit_line_vals})
        res.update({'debit_line_vals': debit_line_vals})
        return res
