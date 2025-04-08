from odoo import fields, models, api


class MrpReport(models.Model):
    _inherit = 'mrp.report'

    multi_uom_line_id = fields.Many2one('multi.uom.line', 'UOM')


    def _select(self):
        res = super()._select()
        res['multi_uom_line_id'] = ", wl.multi_uom_line_id AS multi_uom_line_id"
        return res


    def _group_by(self):
        res = super()._group_by()
        res += """,
            wl.multi_uom_line_id
            """
        return res
