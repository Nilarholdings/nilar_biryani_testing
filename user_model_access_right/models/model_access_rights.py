from odoo import models, fields, api


class ModelAccessRight(models.Model):
    _name = 'model.access.right'
    _description = 'Controls Model Options ( Create, Edit, Delete ) to user.'

    employee_id = fields.Many2one('hr.employee', string='Employee', readonly=True)
    model_id = fields.Many2one('ir.model', ondelete='cascade', required=True, help="select the model")
    can_delete = fields.Boolean(string="Delete", help="Hide the delete option")
    can_create = fields.Boolean(string="Create", help="Hide the create option from list/form view")
    can_edit = fields.Boolean(string="Edit", help="Hide the edit option from list/form view")
