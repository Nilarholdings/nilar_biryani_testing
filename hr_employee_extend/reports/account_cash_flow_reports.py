from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.http import request


class AccountCashFlowReport(models.AbstractModel):
    _inherit = 'account.cash.flow.report'

    @api.model
    def _get_filter_journals(self):
        journals = []
        # OVERRIDE to filter only bank / cash journals.
        emp = self.env.user
        journals = self.env['account.journal'].search([
            ('company_id', 'in', self.env.companies.ids),
            ('type', 'in', ('bank', 'cash')),
        ], order='company_id, name')
        if journals:
            if emp and emp.journal_ids:
                return journals.filtered(lambda l: l.id in emp.journal_ids.ids)
            else:
                raise UserError(_("Please add journals first!!"))
        else:
            raise UserError(_("You must have journals!!"))
