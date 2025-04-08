from odoo import models, fields, api, _


class AccountAnalytic(models.Model):
    _inherit = 'account.analytic.account'

    from_shop_ph = fields.Char('မှာသည့်ဆိုင်ဖုန်း')
    shop_to_take_id = fields.Many2one('shop.to.take', 'ယူမည့်ဆိုင်')
    shop_to_take_ph = fields.Char('ယူမည့်ဆိုင်ဖုန်း')

    @api.model
    def create(self, vals):
        analytic_account_id = super(AccountAnalytic, self).create(vals)
        self.env.user.write({'allow_analytic_account_id': [(4, analytic_account_id.id)]})
        return analytic_account_id

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if not self.env.is_admin():
            if not args:
                args = []
            args.append(
                ('id', 'in', self.env.user.allow_analytic_account_id.ids)
            )

        return super(AccountAnalytic, self)._search(args, offset=offset, limit=limit,
                                                     order=order, count=count,
                                                     access_rights_uid=access_rights_uid)

    @api.onchange('shop_to_take_id')
    def onchange_shop_to_take_ph(self):
        shop = []
        for rec in self:
            if rec.shop_to_take_id:
                self.shop_to_take_ph = rec.shop_to_take_id.phone

