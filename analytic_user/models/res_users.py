from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    def_analytic_account_id = fields.Many2one('account.analytic.account',
                                              'Default Analytic Account')
    allow_analytic_account_id = fields.Many2many('account.analytic.account', 'analytic_account_res_user_rel', 'user_id', 'analytic_account_id',
                                                 string='Allow Analytic Account')

    journal_ids = fields.Many2many('account.journal', 'account_journal_user_rel', 'user_id',
                                   'journal_id', string="Allow Journal")
    default_journal_id = fields.Many2one('account.journal', string="Default Journal")
    pos_location_ids = fields.Many2many('pos.location', 'pos_location_user_rel', 'user_id', 'pos_location_id',
                                        'Allow Pos Counter Location')