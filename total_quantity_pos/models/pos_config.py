# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2023-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ammu Raj (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
from odoo import fields, models, api


class PosConfig(models.Model):
    """ Class for adding the fields in the pos config"""
    _inherit = "pos.config"

    pos_total_screen = fields.Boolean(string="Total Items and Quantity",
                                      help="Enable this option will show the"
                                           "total number of items and total"
                                           "quantities of product in the PoS"
                                           "screen.")
    pos_total_receipt = fields.Boolean(string="Total Items and Quantity",
                                       help="Enable this option will show the"
                                            "total number of items and total"
                                            "quantities of product in the"
                                            "receipt.")

class POSOrder(models.Model):
     _inherit = 'pos.order'

     total_wo_taxes = fields.Float("Total W/O Tax",compute="compute_total_without_tax",store=True)

     @api.depends('amount_tax')
     def compute_total_without_tax(self):
          for rec in self:
               total_wo_taxes = 0.0
               if rec.lines:
                    for line in rec.lines:
                         total_wo_taxes += line.price_subtotal
               rec.total_wo_taxes = total_wo_taxes
