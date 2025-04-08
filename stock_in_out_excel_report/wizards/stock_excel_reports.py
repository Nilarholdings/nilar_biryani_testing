from odoo import api, models, fields
from dateutil.relativedelta import relativedelta

class StockDetailReportWizard(models.TransientModel):
	_name = 'stock.excel.reports'
	_description = 'Stock Excel Reports'

	location_ids = fields.Many2many('stock.location', string='Locations', domain=[('usage', '=', 'internal')])
	product_ids = fields.Many2many('product.product', string='Products', domain=[('detailed_type', '=', 'product')])
	
	start_date = fields.Date('Start Date',
                             required=True,
                             default=lambda self: fields.Date.context_today(self).replace(day=1))
	end_date = fields.Date('End Date',
                           required=True,
                           default=lambda self: fields.Date.context_today(self) + relativedelta(day=31))

	def btn_print(self):
		if not self.location_ids:
			data = {
				'start_date': self.start_date,
				'end_date': self.end_date,
				'location_ids': '',
				'product_ids': self.product_ids.ids,
			}			
		else:
			data = {
				'start_date': self.start_date,
				'end_date': self.end_date,
				'location_ids': self.location_ids and self.location_ids.ids,
				'product_ids': self.product_ids.ids,
			}		
		return self.env.ref('stock_in_out_excel_report.report_stock_in_out_report').report_action(docids=[], data=data)
		


