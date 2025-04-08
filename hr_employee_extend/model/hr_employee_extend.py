from odoo import models,fields,api,_


class HrEmployeePrivate(models.Model):
    _inherit = 'hr.employee'

    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', check_company=True)
    location_id = fields.Many2one('stock.location', string='Location')
    user_signature = fields.Binary(string="User Signature")

