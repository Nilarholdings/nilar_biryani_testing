# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    control_model_actions = fields.Boolean(string="Control models' actions")
    model_access_right_lines = fields.Many2many('model.access_right.lines',
                                                default=lambda self: self.env['model.access_right.lines'].search(
                                                    []).ids)

    @api.model
    def check_model_access_right(self, model_name):
        # If admin, bypass Readonly

        if self.env.is_admin(): return {'can_create': True, 'can_edit': True, 'can_delete': True}
        emp = self.env.user.get_employee_login()['emp_id']
        if emp:
            # If control_model_actions is not checked, allow to do actions
            employee = self.env['hr.employee'].browse(emp)
            if not employee.control_model_actions: return {'can_create': True, 'can_edit': True, 'can_delete': True}

            model_access_right_lines = employee.model_access_right_lines

            exist = True if model_name in model_access_right_lines.mapped('model_id').mapped('model') else False

            vals = {}
            if exist:
                request_model = model_access_right_lines.filtered(lambda l: l.model_id.model == model_name)[-1]
                vals = {
                    'can_create': request_model.can_create,
                    'can_edit': request_model.can_edit,
                    'can_delete': request_model.can_delete,
                }

            return vals
        else:
            return {'can_create': True, 'can_edit': True, 'can_delete': True}


class ModelAccessRightLines(models.Model):
    _name = 'model.access_right.lines'
    _description = 'Model Access Right Lines'

    model_id = fields.Many2one('ir.model', string='Model')
    can_create = fields.Boolean('Can Create', default=False)
    can_edit = fields.Boolean('Can Edit', default=False)
    can_delete = fields.Boolean('Can Delete', default=False)

    _sql_constraints = [
        (
            'unique_model_id',
            'unique(model_id)',
            'Model already exist !'
        ),
    ]
