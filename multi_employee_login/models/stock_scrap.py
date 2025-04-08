from odoo import models, fields, api
from odoo.http import request


class Stock_Scrap(models.Model):

    _inherit = 'stock.scrap'

    def action_validate(self):
        res = super(Stock_Scrap, self).action_validate()
        message = (f"Validate By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res