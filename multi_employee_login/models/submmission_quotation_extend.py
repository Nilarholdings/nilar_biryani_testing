from odoo import models, fields, api, _
from odoo.http import request


class SubmissionQuotation(models.Model):
    _inherit = 'submission.quotation'

    def action_submit(self):
        res = super(SubmissionQuotation, self).action_submit()
        message = (f"Submit By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_confirm(self):
        res = super(SubmissionQuotation, self).action_confirm()
        message = (f"Confirm By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_checked(self):
        res = super(SubmissionQuotation, self).action_checked()
        message = (f"Checked By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_approved(self):
        res = super(SubmissionQuotation, self).action_approved()
        message = (f"Approved By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res

    def action_cancel(self):
        res = super(SubmissionQuotation, self).action_cancel()
        message = (f"Cancel By: ==> {self.env.user.employee_id.name}")
        self.message_post(body=message)
        return res
