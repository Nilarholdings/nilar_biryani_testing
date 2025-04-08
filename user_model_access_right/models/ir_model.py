# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class IRModel(models.Model):
    _inherit = 'ir.model'
    _rec_name = 'name_to_show'

    name_to_show = fields.Char(compute='_compute_name_to_show')

    @api.depends('name', 'model')
    def _compute_name_to_show(self):
        for rec in self:
            rec.name_to_show = f'{rec.name} ( {rec.model} )'
