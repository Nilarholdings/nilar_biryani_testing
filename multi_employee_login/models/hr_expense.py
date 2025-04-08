from odoo import models, fields, api
from odoo.http import request


class HrExpense(models.Model):
    _inherit = "hr.expense"

    #@api.onchange('company_id')
    #def _onchange_expense_company_id(self):
    #    if self.env.user:
    #        self.employee_id = self.env.user.id
    #    else:
    #        self.employee_id = self.env['hr.employee'].search(
    #            [('user_id', '=', self.env.uid), ('company_id', '=', self.company_id.id)])
