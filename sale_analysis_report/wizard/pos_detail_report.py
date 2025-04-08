from datetime import datetime, time
from dateutil import relativedelta
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _


class PosDetailReportWizard(models.TransientModel):
    _name = 'pos.detail.report'
    _description = 'POS Detail Reports'

    def _default_date_from(self):
        today = fields.Date.today()
        return fields.datetime.combine(today, time.min)-relativedelta(hours=6, minutes=30)

    def _default_date_to(self):
        today = fields.Date.today()
        return fields.datetime.combine(today, time.max)-relativedelta(hours=6, minutes=30)

    date_from = fields.Datetime('Date From', required=True, default=_default_date_from)
    date_to = fields.Datetime('Date To', required=True, default=_default_date_to)
    analytic_account_id = fields.Many2many('account.analytic.account', string='Analytic Accounts')

    def btn_print(self):
        return self.env.ref('sale_analysis_report.pos_analysis_excel_report').report_action(self, data={
            'date_from': self.date_from,
            'date_to': self.date_to,
            'analytic_account_id': self.analytic_account_id.ids
        })
