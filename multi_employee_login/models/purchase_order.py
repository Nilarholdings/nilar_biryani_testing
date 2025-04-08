from odoo import models, fields, api, _
from odoo.http import request
from odoo.fields import Date
from odoo.exceptions import UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        res = super(PurchaseOrder, self).create(vals)
        message = (f"Create By: ==> {self.env.user.employee_id.name}")
        res.message_post(body=message)
        return res

    def action_confirm(self):
        res = super(PurchaseOrder, self).action_confirm()
        message = (f"Confrim By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_verified(self):
        res = super(PurchaseOrder, self).action_verified()
        message = (f"Verified By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        message = (f"Approved By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_view_invoice(self, invoices=False):
        """
        Inherited for adding relation with ICT if created by it.
        @author: Maulik Barad on Date 16-Oct-2019.
        @return: Action for displaying vendor bill for purchase order.
        """
        action = super(PurchaseOrder, self).action_view_invoice(invoices)
        message = (f"Create Bill By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        if self.env.context.get('create_bill', False):
            ctx = eval(action['context'])
            action['context'] = ctx
        return action

    @api.onchange('user_id')
    def onchange_employee(self):
        employee_id = self.env.user.employee_id
        self.prepare_by_date = Date.today()
        self.prepare_by_name = employee_id.id


class StockRequestion(models.Model):
    _inherit = 'stock.requestion'

    @api.model
    def create(self, vals):
        res = super(StockRequestion, self).create(vals)
        message = (f"Create By: ==> {self.env.user.employee_id.name}")
        res.message_post(body=message)
        return res

    def action_draft(self):
        res = super(StockRequestion, self).action_draft()
        message = (f"Draft By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_submit(self):
        res = super(StockRequestion, self).action_submit()
        message = (f"Submit By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_cancel(self):
        res = super(StockRequestion, self).action_cancel()
        message = (f"Cancel By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_verified(self):
        res = super(StockRequestion, self).action_verified()
        message = (f"Verified By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_approved(self):
        res = super(StockRequestion, self).action_approved()
        message = (f"Approved By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_confirm(self):
        res = super(StockRequestion, self).action_confirm()
        message = (f"Confirm By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res



class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    @api.model
    def create(self, vals):
        res = super(PurchaseRequisition, self).create(vals)
        message = (f"Create By: ==> {self.env.user.employee_id.name}")
        res.message_post(body=message)
        return res

    def action_in_progress(self):
        res = super(PurchaseRequisition, self).action_in_progress()
        message = (f"Progress By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_open(self):
        res = super(PurchaseRequisition, self).action_open()
        message = (f"Open By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_done(self):
        res = super(PurchaseRequisition, self).action_done()
        message = (f"Done By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res



