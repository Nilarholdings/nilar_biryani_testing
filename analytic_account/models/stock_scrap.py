from odoo import api, models, fields, _ 
from odoo.http import request

class StockScrap(models.Model):

    _inherit = 'stock.scrap'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')

    def do_scrap(self):
        res = super(StockScrap, self).do_scrap()
        if not self.analytic_account_id:
            return res
        account_moves = self.env['account.move'].search([('stock_move_id.id', '=', self.move_id.id)])
        for account_move in account_moves:
            account_move.analytic_account_id = self.analytic_account_id.id
        return res

    @api.model
    def default_get(self, fields_list):
        vals = super(StockScrap, self).default_get(fields_list)
        default_analytic_account_id = False
        if self.env.user:
            employee_id = self.env.user
            analytic_id = employee_id.def_analytic_account_id.id
            if analytic_id:
                default_analytic_account_id = analytic_id
        if default_analytic_account_id:
            vals.update({'analytic_account_id': default_analytic_account_id})
        return vals
