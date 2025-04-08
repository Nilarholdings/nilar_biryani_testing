from odoo import models, fields, api, _
from odoo.http import request


class PurchaseStockRequisition(models.Model):
    _inherit = 'purchase.stock.requisition'

    @api.model
    def create(self, vals):
        res = super(PurchaseStockRequisition, self).create(vals)
        message = (f"Create By: ==> {self.env.user.employee_id.name}")
        res.message_post(body=message)
        return res

    def action_confirm(self):
        res = super(PurchaseStockRequisition, self).action_confirm()
        message = (f"Confirm By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_verified(self):
        res = super(PurchaseStockRequisition, self).action_verified()
        message = (f"Verified By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_approved(self):
        res = super(PurchaseStockRequisition, self).action_approved()
        message = (f"Approved By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_checked(self):
        res = super(PurchaseStockRequisition, self).action_checked()
        message = (f"Checked By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_cancel(self):
        res = super(PurchaseStockRequisition, self).action_cancel()
        message = (f"Cancel By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res




