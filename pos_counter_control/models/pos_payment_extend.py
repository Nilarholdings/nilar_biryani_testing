from odoo import models, fields, api, _
from odoo.http import request


class PosPayment(models.Model):
    _inherit = 'pos.payment'

    def check_access_payment(self):
        if self.env.user:
            allow_pos_locations = self.env.user.pos_location_ids.ids

            if allow_pos_locations:
                return {
                    'type': 'ir.actions.act_window',
                    'name': ('Payments'),
                    'res_model': 'pos.payment',
                    'view_mode': 'tree,kanban,form',
                    'domain': [('session_id.config_id.location_id', 'in', allow_pos_locations)],
                    'context': {},
                }
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'name': ('Payments'),
                    'res_model': 'pos.payment',
                    'view_mode': 'tree,kanban,form',
                    'domain': [('session_id.config_id.location_id', 'in', allow_pos_locations)],
                    'context': {},
                }
        else:
            pos_counters = self.env['pos.location'].search([])
            return {
                'type': 'ir.actions.act_window',
                'name': ('Payments'),
                'res_model': 'pos.payment',
                'view_mode': 'tree,kanban,form',
                'domain': [('session_id.config_id.location_id', 'in', pos_counters)],
                'context': {},
            }
