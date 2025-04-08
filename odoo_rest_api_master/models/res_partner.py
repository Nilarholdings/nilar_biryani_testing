from odoo import models, fields, api, _

class Partner(models.Model):
    _inherit = 'res.partner'

    x_city_id = fields.Many2one('res.city', string='City', domain="[('state_id', '=?', state_id)]", ondelete='restrict')

    @api.onchange('state_id')
    def _onchange_states_id(self):
        if self.state_id and self.state_id != self.x_city_id.state_id:
            self.x_city_id = False
    @api.onchange('x_city_id')
    def onchange_state(self):
        self.city = self.x_city_id.name
        self.state_id = self.x_city_id.state_id
        self.country_id = self.x_city_id.country_id


