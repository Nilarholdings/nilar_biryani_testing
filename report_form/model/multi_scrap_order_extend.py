import datetime
from odoo import models, fields, api, _
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class PurchaseOrder(models.Model):
    _inherit = 'stock.multi.scrap'

    def get_multi_scrap_order_pdf_report(self):
        index = 1
        records = []

        for order in self:
            line_ids = []
            for line in order.line_ids:
                line_ids.append({
                    'sr': index,
                    'product': line.product_id.name or '',
                    'qty': "{:,.0f}".format(line.scrap_qty) or 0.00,
                    'uom': line.product_uom_id.name if line.product_uom_id else '',
                    'source': line.location_id.complete_name or '',
                    'scrap_location': line.scrap_location_id.complete_name or '',
                    'remark': line.remark or '',
                 
                   
                })
                index += 1

            records.append({
                'document_no': order.document_number or '',
                'excepted_date': (order.excepted_date + relativedelta(hours=6, minutes=30)).strftime('%m/%d/%Y %H:%M:%S') or '',
                'analytic_account_id': order.analytic_account_id.name if order.analytic_account_id else '',                 
                'analytic_tag_ids': order.analytic_tag_ids.name if order.analytic_tag_ids else '',
                'prepared_by_sign': order.prepare_employee_sign,
                'prepared_by_date': order.prepare_date,
                'prepared_by_name': order.prepare_employee_id.name,
                'verified_by_sign': order.verified_employee_sign,
                'verified_by_date': order.verified_date,
                'verified_by_name': order.verified_employee_id.name,
                'approved_by_sign': order.approve_employee_sign,
                'approved_by_date': order.approve_date,
                'approved_by_name': order.approve_employee_id.name,
                'line_ids': line_ids,
            })
        return self.env.ref('report_form.action_multi_scrap_order_pdf_report').report_action(self,
                                                                                          data={'records': records})
