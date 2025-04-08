from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MarketingCustomer(models.Model):
    _inherit = 'res.partner'
    x_marketing_customer = fields.Boolean(string="Marketing Customer")


