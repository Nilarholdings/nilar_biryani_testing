from odoo import models, fields, api
from odoo.http import request


class Stock_Picking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(Stock_Picking, self).button_validate()
        for pick in self:
            message = (f"Validate By: ==> {pick.env.user.employee_id.name}")
            pick.message_post(body=message)
        return res

    def action_assign_way(self):
        res = super(Stock_Picking, self).action_assign_way()
        message = (f"Assign Way By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res



