from odoo import models, fields, api, _


class ProductGroup(models.Model):
    _name = 'product.group'
    _description = 'Product Group'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'This Name Already Exit!'),
    ]
