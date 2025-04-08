import datetime
from odoo import models, fields, api, _
from datetime import timedelta


class PurchaseOrder(models.Model):
    _inherit = 'hr.expense.sheet'

    def get_hr_expense_sheet_pdf_report(self):
        index = 1
        records = []
        for order in self: 
            expense_line_ids = []
            for line in order.expense_line_ids:
                expense_line_ids.append({
                    'date': (line.date + timedelta(hours=6, minutes=30)).strftime(
                       "%m/%d/%Y") if line.date else '',
                    'product': line.product_id.name or '',
                    'description': line.name or '',
                    'analytic_account_id': line.analytic_account_id.name if line.analytic_account_id else '',                 
                    'ref': line.reference or '',
                    'uni_amt': "{:,.0f}".format(line.unit_amount) or 0.00,
                    'tax': line.tax_ids or 0.00,
                    'qty': "{:,.0f}".format(line.quantity) or 0.00,                
                    'total_amount': "{:,.0f}".format(line.total_amount_company) or 0.00,
                })
                index += 1
            if order.payment_mode == 'own_account' : 
                records.append({                    
                    'employees': order.employee_id.name or '',
                    'rec_description': order.name or '',
                    'accounting_date': (order.accounting_date + timedelta(hours=6, minutes=30)).strftime(
                           "%m/%d/%Y") if order.accounting_date else '',
                    'velidated_by': order.user_id.name or '' ,
                    'payment_by' : 'Employee (to reimburse)',
                    'amount': "{:,.0f}".format(order.total_amount) or 0.00,
                    'expense_line_ids':expense_line_ids,
                })

            else:
                records.append({
                    'employees': order.employee_id.name or '',
                    'rec_description': order.name or '',
                    'accounting_date': (order.accounting_date + timedelta(hours=6, minutes=30)).strftime(
                           "%m/%d/%Y") if order.accounting_date else '',
                    'velidated_by': order.user_id.name or '' ,
                    'payment_by' : 'Company',
                    'amount': "{:,.0f}".format(order.total_amount) or 0.00,
                    'expense_line_ids':expense_line_ids,
                })

        return self.env.ref('report_form.action_hr_expense_sheet_pdf_report').report_action(self,
                                                                                          data={'records': records})
