from odoo import models, fields, api, _


class AccountMoveLineUpdate(models.Model):
    _name = 'account.move.line.update'
    _description = 'Account Move Line Update'

    account_id = fields.Many2one('account.account', 'Update Account', required=True)

    def apply_update_account(self):
        selected_lines = self._context.get('active_ids')
        move_lines = self.env['account.move.line'].browse(selected_lines)

        for line in move_lines:
            line.write({
                'account_id': self.account_id.id,
            })
