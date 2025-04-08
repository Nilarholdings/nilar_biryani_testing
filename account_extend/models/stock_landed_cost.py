from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    @api.model
    def default_get(self, fields_list):
        vals = super(StockLandedCost, self).default_get(fields_list)
        default_journal_id = False
        journal_id = self.env['ir.property']._get("property_stock_journal", "product.category")
        default_journal_id = journal_id
        if default_journal_id:
            vals.update({'account_journal_id': default_journal_id})
        return vals

    @api.onchange('account_journal_id')
    def onchange_journal(self):
        return {'domain': {'account_journal_id': [('id', 'in', self.env.user.journal_ids.ids)]}}

    def write(self, vals):
        res = super(StockLandedCost, self).write(vals)
        if self.account_journal_id:
            if self.env.user:
                journal_ids = self.env.user.journal_ids.ids
                if not journal_ids:
                    raise ValidationError(
                        _("Journal Name -%s is not include allow journal access of  Employee - ( %s)!" % (
                        self.account_journal_id.name, self.env.user.name)))
        return res
