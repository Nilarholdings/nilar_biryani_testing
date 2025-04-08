from odoo import api, models, fields
from odoo.http import request


class PosOrder(models.Model):
    _inherit = 'pos.order'
    config_id = fields.Many2one('pos.config', string='POS Config ID', related='session_id.config_id', store=True)
    location_id = fields.Many2one('pos.location', string='Location ID', related='config_id.location_id', store=True)

    def check_access_order(self):
        if self.env.user:
            allow_pos_locations = self.env.user.pos_location_ids.ids
            if allow_pos_locations:
                return {
                    'type': 'ir.actions.act_window',
                    'name': ('Orders'),
                    'res_model': 'pos.order',
                    'view_mode': 'tree,form,kanban,pivot',
                    'domain': [('location_id', 'in', allow_pos_locations)],
                    'context': {},
                }
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'name': ('Orders'),
                    'res_model': 'pos.order',
                    'view_mode': 'tree,form,kanban,pivot',
                    'domain': [('location_id', 'in', allow_pos_locations)],
                    'context': {},
                }
        else:
            pos_counters = self.env['pos.location'].search([])
            return {
                'type': 'ir.actions.act_window',
                'name': ('Orders'),
                'res_model': 'pos.order',
                'view_mode': 'tree,form,kanban,pivot',
                'domain': [('location_id', 'in', pos_counters)],
                'context': {},
            }


class PosSession(models.Model):
    _inherit = 'pos.session'

    def check_access_pos_session(self):
        if self.env.user:
            allow_pos_locations = self.env.user.pos_location_ids.ids

            if allow_pos_locations:
                return {
                    'type': 'ir.actions.act_window',
                    'name': ('Sessions'),
                    'res_model': 'pos.session',
                    'view_mode': 'tree,kanban,form',
                    'domain': [('config_id.location_id', 'in', allow_pos_locations), ],
                    'context': {},
                }
            else:
                return {
                    'type': 'ir.actions.act_window',
                    'name': ('Sessions'),
                    'res_model': 'pos.session',
                    'view_mode': 'tree,kanban,form',
                    'domain': [('config_id.location_id', 'in', allow_pos_locations), ],
                    'context': {},
                }
        else:
            pos_counters = self.env['pos.location'].search([])
            return {
                'type': 'ir.actions.act_window',
                'name': ('Sessions'),
                'res_model': 'pos.session',
                'view_mode': 'tree,kanban,form',
                'domain': [('config_id.location_id', 'in', pos_counters), ],
                'context': {},
            }
