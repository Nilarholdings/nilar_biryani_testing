import datetime
from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    def get_vendor_bill_a4(self):
        records = []
        for order in self:
            invoice_line_ids = []
            paid = 0.00
            no = 1
            for line in order.invoice_line_ids:
                invoice_line_ids.append({
                    'no': no,
                    'product': line.product_id.name if line.product_id else line.name,
                    'code': line.product_id.default_code if line.product_id else '',
                    'discount': '{0:,.2f}'.format(line.discount_amount),
                    'qty': '{0:,.2f}'.format(line.multi_uom_qty),
                    'uom': line.multi_uom_line_id.uom_id.name if line.multi_uom_line_id else '',
                    'price_unit': '{0:,.2f}'.format(line.multi_price_unit) if line.multi_price_unit else '0.00',
                    'subtotal': '{0:,.2f}'.format(line.price_subtotal) if line.price_subtotal else '0.00',
                })
                no += 1

            for payment in self.sudo()._get_reconciled_info_JSON_values():
                paid += payment['amount']

            records.append({
                'name': order.name,
                'origin': order.invoice_origin,
                'partner': order.partner_id.name if order.partner_id else '',
                'picking': order.picking_number,
                'payment_term': order.invoice_payment_term_id.name if order.invoice_payment_term_id else '',
                'employee': order.user_id.employee_id.name if order.user_id.employee_id else '',
                'analytic': order.analytic_account_id.name if order.analytic_account_id else '',
                'date': (order.invoice_date + timedelta(hours=6, minutes=30)).strftime("%d-%m-%Y") if order.invoice_date else '',
                'paid_amount': '{0:,.2f}'.format(paid) or '0.00',
                'total': '{0:,.2f}'.format(order.amount_total) if order.amount_total else '0.00',
                'amount_due': '{0:,.2f}'.format(order.amount_residual) if order.amount_residual else '0.00',
                'lines': invoice_line_ids,
            })

        return self.env.ref('report_form.action_vendor_bill_a4').report_action(self, data={'records': records})

