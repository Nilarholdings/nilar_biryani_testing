from odoo import fields, models, api, _

class DataResponsible(models.Model):
    _name = 'data.responsible'
    _description = 'Responsible Person/Group/Department for Master Data'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Responsible Name',tracking=True)

class MasterDataResponsible(models.Model):
    _name = 'master.data.responsible'
    _description = 'Responsible record for Master Data'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char('Master Data Name')
    responsible_ids = fields.Many2many('data.responsible','master_data_respon_rel',string='Responsibles')

