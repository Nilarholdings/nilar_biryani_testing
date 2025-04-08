from odoo import models, fields, api, _
from odoo.http import request


class AccountAsset(models.Model):
    _inherit = 'account.asset'

    @api.model
    def default_get(self, fields_list):
        vals = super(AccountAsset, self).default_get(fields_list)
        default_journal_id = False
        journal_id = self.env.user.journal_ids.filtered(lambda l: l.type == 'general')
        if journal_id:
            default_journal_id = journal_id[0]
        if default_journal_id:
            vals.update({'journal_id': default_journal_id})
        return vals

    @api.onchange('method', 'journal_id')
    def onchange_journal(self):
        for rec in self:
            journal_ids = rec.env.user.journal_ids.filtered(lambda l: l.type == 'general')
            return {'domain': {'journal_id': [('id', 'in', journal_ids.ids)]}}
