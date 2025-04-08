from odoo import models, fields, api, _


class HrExpense(models.Model):
    _inherit = "hr.expense"

    employee_id = fields.Many2one('hr.employee', string="Employee",
                                  store=True, required=True, readonly=False, tracking=True,
                                  states={'approved': [('readonly', True)], 'done': [('readonly', True)]},
                                  check_company=True)