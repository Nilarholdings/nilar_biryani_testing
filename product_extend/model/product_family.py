from odoo import models, fields, api, _


class ProductFamily(models.Model):
    _name = 'product.family'
    _description = 'Product Family'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", tracking=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'This Name Already Exit!'),
    ]
