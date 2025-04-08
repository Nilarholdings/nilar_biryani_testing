from odoo import fields, models, api
from odoo.exceptions import UserError
from odoo.http import request


class AccountBankStatement(models.Model):
    _inherit = 'account.bank.statement'

    journals_ids = fields.Many2many('account.journal', 'Access Journals', compute='compute_journals')

    @api.depends('company_id')
    def compute_journals(self):
        for rec in self:
            emp = self.env.user
            if emp and emp.journal_ids:
                rec.journals_ids = emp.journal_ids.ids
            else:
                rec.journals_ids = []


