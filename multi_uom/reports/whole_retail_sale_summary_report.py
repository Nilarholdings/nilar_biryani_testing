from odoo import models, fields, api, _

import logging

_logger = logging.getLogger(__name__)


class WholeRetailSummaryReport(models.Model):
    _inherit = 'whole.retail.summary.report'

    multi_uom_line_id = fields.Many2one('multi.uom.line', 'UOM', required=False)

