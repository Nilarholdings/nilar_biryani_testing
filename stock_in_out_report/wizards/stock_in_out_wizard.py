from odoo import api, models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta


class StockInOutWizard(models.TransientModel):

    _name = 'stock.in.out.wizard'
    _description = 'Stock In/Out Wizard'

    start_date = fields.Date('Beginning Date',
                             required=True,
                             default=lambda self: fields.Date.context_today(self).replace(day=1))
    end_date = fields.Date('End Date',
                           required=True,
                           default=lambda self: fields.Date.context_today(self) + relativedelta(day=31))
    location_ids = fields.Many2many('stock.location', string='Locations', required=False)
    product_ids = fields.Many2many('product.product', string='Products', domain=[('detailed_type', '=', 'product')])

    def btn_print(self):
        if not self.product_ids:

            product_ids = self.env['product.product'].with_context(active_test=False).search(
                    [('detailed_type', '!=', 'service')])
        else:
            product_ids = self.product_ids
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'location_ids': self.location_ids and self.location_ids.ids or self.available_location_ids.ids,
            'product_ids': product_ids.ids,
        }
        return self.env.ref('stock_in_out_report.report_stock_in_out_report').report_action(docids=[], data=data)
