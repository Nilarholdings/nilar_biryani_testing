from odoo import models,fields,api
from odoo.http import request

class Sale_order_(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(Sale_order_, self).action_confirm()
        message = (f"Confirm By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_sale_requistion(self):
        res = super(Sale_order_, self).action_sale_requistion()
        message = (f"Sale Requisition By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_cancel(self):
        res=super(Sale_order_, self).action_cancel()
        message = (f"Cancel By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def _create_invoices(self, grouped=False, final=False, date=None):
        res = super(Sale_order_, self)._create_invoices(grouped, final, date)
        message = (f"Create Invoice By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res


class WholeSaleRequisition(models.Model):
    _inherit = 'whole.sale.requisition'


    def action_confirm(self):
        res = super(WholeSaleRequisition, self).action_confirm()
        message = (f"Confirm By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_approved(self):
        res = super(WholeSaleRequisition, self).action_approved()
        message = (f"Approved By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_cancel(self):
        res = super(WholeSaleRequisition, self).action_cancel()
        message = (f"Cancel By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res


