from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    pos_location_id = fields.Many2one('pos.location', string='POS Location')


class POSLocation(models.Model):
    _inherit = 'pos.location'

    location_id = fields.Many2one('stock.location', string='Location')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic')
    quant_ids = fields.One2many('stock.quant', 'pos_location_id', string='Quant')


    @api.onchange('location_id')
    def onchange_location(self):
        if self.location_id:
            quant = self.env['stock.quant'].search([('location_id', '=', self.location_id.id)])
            self.quant_ids = [(6, 0, quant.ids)]
        else:
            self.quant_ids = [(5, 0, 0)]

    def write(self, vals):
        if 'location_id' in vals:
            new_location_id = vals['location_id']
            for record in self:
                if record.location_id.id != new_location_id:
                    quant = self.env['stock.quant'].search([('location_id', '=', new_location_id)])
                    vals['quant_ids'] = [(6, 0, quant.ids)]
        return super(POSLocation, self).write(vals)

    def action_get_stock_quant(self):
        action = self.env['ir.actions.act_window']._for_xml_id('stock.location_open_quants')
        action['domain'] = [('pos_location_id', '=', self.id)]
        return action
