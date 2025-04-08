import pytz
from datetime import datetime
from collections import defaultdict
from odoo import api, fields, models
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import clean_context, OrderedSet
from odoo.tools.float_utils import float_compare, float_is_zero, float_round


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_common_svl_vals(self):
        res = super(StockMove, self)._prepare_common_svl_vals()
        if self.picking_id:
            res['date'] = self.picking_id.scheduled_date
            res['analytic_account_id'] = self.picking_id.analytic_account_id.id
        elif self.scrapped:
            res['date'] = self._context.get('force_period_date')
        elif self.scrapped:
            res['date'] = self._context.get('force_period_date')
        elif self.is_inventory:
            res['date'] = self._context.get('force_period_date')
        elif self.production_id:
            res['date'] = self.production_id.date_planned_start
        elif self.raw_material_production_id:
            res['date'] = self.raw_material_production_id.date_planned_start
        elif self.created_production_id:
            res['date'] = self.created_production_id.date_planned_start
        else:
            res['date'] = self.date
            res['analytic_account_id'] = self.analytic_account_id.id
        return res

    def _prepare_account_move_vals(self, credit_account_id, debit_account_id, journal_id, qty, description, svl_id,
                                   cost):
        self.ensure_one()
        move_lines = self._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
        if move_lines:
            date = self._context.get('force_period_date', False)

            if not date and self.picking_id:
                picking_date = self.picking_id.scheduled_date

                local_tz_st = pytz.timezone(self.env.user.tz or 'UTC')
                if picking_date:
                    scheduled_date_only = picking_date
                    start_d = scheduled_date_only.replace(tzinfo=pytz.utc).astimezone(local_tz_st)
                    start_date = datetime.strftime(start_d, DEFAULT_SERVER_DATETIME_FORMAT)
                    scheduled_date_only = datetime.strptime(
                        start_date, '%Y-%m-%d %H:%M:%S'
                    )
                    date = scheduled_date_only.date()

            if not date and self.date:
                picking_date = self.date

                local_tz_st = pytz.timezone(self.env.user.tz or 'UTC')
                if picking_date:
                    scheduled_date_only = picking_date
                    start_d = scheduled_date_only.replace(tzinfo=pytz.utc).astimezone(local_tz_st)
                    start_date = datetime.strftime(start_d, DEFAULT_SERVER_DATETIME_FORMAT)
                    scheduled_date_only = datetime.strptime(
                        start_date, '%Y-%m-%d %H:%M:%S'
                    )
                    date = scheduled_date_only.date()

            return {
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': description,
                'stock_move_id': self.id,
                'analytic_account_id': self.analytic_account_id.id,
                'stock_valuation_layer_ids': [(6, None, [svl_id])],
                'move_type': 'entry',
            }


