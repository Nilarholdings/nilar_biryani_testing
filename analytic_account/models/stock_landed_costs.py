from odoo import api, models, fields, _
from odoo.http import request


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')

    def button_validate(self):
        res = super(StockLandedCost, self).button_validate()
        for pick in self:
            if not pick.analytic_account_id or not pick.account_move_id:
                return res
            pick.account_move_id.analytic_account_id = pick.analytic_account_id.id
        return res

    @api.model
    def default_get(self, fields_list):
        vals = super(StockLandedCost, self).default_get(fields_list)
        default_analytic_account_id = False
        if self.env.user:
            employee_id = self.env.user
            analytic_id = employee_id.def_analytic_account_id.id
            if analytic_id:
                default_analytic_account_id = analytic_id
        if default_analytic_account_id:
            vals.update({'analytic_account_id': default_analytic_account_id})
        return vals

