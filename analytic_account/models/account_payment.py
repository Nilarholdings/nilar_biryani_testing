from odoo import api, models, fields, _ 


class AccountPayment(models.Model):

    _inherit = 'account.payment'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account')

    def action_post(self):
        res = super(AccountPayment, self).action_post()
        for payment in self:
            payment.move_id.write({'analytic_account_id': payment.analytic_account_id.id})
        return res


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    @api.model
    def default_get(self, fields_list):
        vals = super(AccountPaymentRegister, self).default_get(fields_list)
        default_journal_id = self.env.user.default_journal_id
        if default_journal_id:
            vals.update({'journal_id': default_journal_id.id})
        return vals