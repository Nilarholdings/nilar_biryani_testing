from odoo import api, models, fields, _
from odoo.http import request


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')

    @api.model
    def _get_inventory_fields_create(self):
        """ Returns a list of fields user can edit when he want to create a quant in `inventory_mode`.
        """
        res = super(StockQuant, self)._get_inventory_fields_create()
        return res + ['analytic_account_id']

    @api.model
    def default_get(self, fields_list):
        vals = super(StockQuant, self).default_get(fields_list)
        default_analytic_account_id = False
        if self.env.user:
            employee_id = self.env.user
            analytic_id = employee_id.def_analytic_account_id.id
            if analytic_id:
                default_analytic_account_id = analytic_id
        if default_analytic_account_id:
            vals.update({'analytic_account_id': default_analytic_account_id})
        return vals
