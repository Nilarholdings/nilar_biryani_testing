from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.tools import float_compare, float_round
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remark = fields.Text(string='Remark')

    sale_picking = fields.Selection([
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
    ], string='Picking Type')

    contact_partner_id = fields.Char(string='Contact Address', compute='_get_contact_address', store=True)
    contact_ph = fields.Char(string='Contact Phone', store=True)

    from_shop_ph = fields.Char(string='မှာသည့်ဆိုင်ဖုန်း')
    to_shop_name = fields.Many2one('shop.to.take', 'ယူမည့်ဆိုင်')
    to_shop_ph = fields.Char('ယူမည့်ဆိုင်ဖုန်း')

    client_name = fields.Char(string='အမည်')
    client_related = fields.Char(string='တော်စပ်ပုံရာထူး')
    client_phone = fields.Char(string='ဖုန်း')
    actual_start_time = fields.Char(string='အမှန်တကယ် စတင်ကျွေးမည့်အချိန်')
    analytic_account_id = fields.Many2one(
        'account.analytic.account', 'Analytic Account',
        readonly=True, copy=True, check_company=True,  # Unrequired company
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help="The analytic account related to a sales order.")
    state = fields.Selection(selection_add=[('confirm', 'Confirm'),
                                            ('verified', 'Verified'),
                                            ('sale', 'Sale')])

    approve_user_id = fields.Many2one('res.users', string='To Approve', tracking=True, default=False,copy=False)

    def confirm_so(self):
        self.write({'state': 'confirm'})

    def verify_so(self):
        self.write({'state': 'verified'})

    @api.depends('partner_id')
    def _get_contact_address(self):
        for rec in self:
            rec.contact_partner_id = False
            if rec.partner_id:
                query = """select name,phone from res_partner rp WHERE rp.parent_id=""" + str(
                    rec.partner_id.id) + """ AND rp.type='contact';"""
                self.env.cr.execute(query)
                result = self.env.cr.dictfetchall()

                for val in result:
                    rec.contact_partner_id = val['name']
                    rec.contact_ph = val['phone']

    def _prepare_invoice(self):
        res = super(SaleOrder, self)._prepare_invoice()
        for rec in self:
            res['analytic_account_id'] = rec.analytic_account_id.id
        return res

    @api.onchange('analytic_account_id')
    def onchange_analytic_acc(self):
        for rec in self:
            rec.warehouse_id = rec.analytic_account_id.location_id.warehouse_id.id
            if rec.analytic_account_id.from_shop_ph:
                rec.from_shop_ph = rec.analytic_account_id.from_shop_ph
            if rec.analytic_account_id.shop_to_take_id:
                rec.to_shop_name = rec.analytic_account_id.shop_to_take_id
            if rec.analytic_account_id.shop_to_take_ph:
                rec.to_shop_ph = rec.analytic_account_id.shop_to_take_ph

    @api.onchange('to_shop_name')
    def onchange_to_shop_ph(self):
        for rec in self:
            rec.to_shop_ph = rec.to_shop_name.phone

    @api.model
    def create(self, vals):
        short_code = self.env['res.company'].browse(vals['company_id']).short_code

        if not short_code:
            raise ValidationError('Please Insert Company Short Code')
        if vals.get('analytic_account_id'):
            branch_code = self.env['account.analytic.account'].browse(vals['analytic_account_id']).short_code
            branch = self.env['account.analytic.account'].browse(vals['analytic_account_id']).name
            if not branch_code:
                raise ValidationError(
                    _(" Please Insert  Branch Code for (%s)" % (branch)))
            else:
                vals['name'] = str(short_code) + '/' + 'SO/' + str(branch_code) + self.env['ir.sequence'].next_by_code(
                    'sale.order') or _(
                    'New')

        res = super(SaleOrder, self).create(vals)
        return res

    order_count = fields.Integer(compute='_compute_orders_number', string='Number of Orders')

    def _compute_orders_number(self):
        for order in self:
            requisition_line = self.env['whole.sale.requisition'].search([('sale_order_id', '=', self.id)])
            order.order_count = len(requisition_line)

    def action_open_requisition_order(self):
        return {
            'type': 'ir.actions.act_window',
            'name': ('Sale Requisition'),
            'res_model': 'whole.sale.requisition',
            'view_mode': 'tree,form',
            'domain': [('sale_order_id', '=', self.id)],
            'context': {
                'default_is_whole_sale': True,
            }
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    remark = fields.Text(string='Remark')

    def _update_line_quantity(self, values):
        orders = self.mapped('order_id')
        for order in orders:
            order_lines = self.filtered(lambda x: x.order_id == order)
            msg = "<b>" + _("The ordered quantity has been updated.") + "</b><ul>"
            for line in order_lines:
                msg += "<li> %s: <br/>" % line.product_id.display_name
                if line.multi_uom_line_id and "multi_uom_line_id" in values:
                    msg += _(
                        "UOM: %(old_uom)s -> %(new_uom)s",
                        old_uom=line.multi_uom_line_id.uom_id.name,
                        new_uom=self.env['multi.uom.line'].browse(values["multi_uom_line_id"]).uom_id.name
                    ) + "<br/>"
                if "multi_uom_qty" in values:
                    msg += _(
                        "Ordered Quantity: %(old_qty)s -> %(new_qty)s",
                        old_qty=line.multi_uom_qty,
                        new_qty=values["multi_uom_qty"]
                    ) + "<br/>"

                # msg += _(
                #     "Ordered Quantity: %(old_qty)s -> %(new_qty)s",
                #     old_qty=line.product_uom_qty,
                #     new_qty=values["product_uom_qty"]
                # ) + "<br/>"

                if line.product_id.type in ('consu', 'product'):
                    msg += _("Delivered Quantity: %s", line.qty_delivered) + "<br/>"
                msg += _("Invoiced Quantity: %s", line.qty_invoiced) + "<br/>"
            precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
            line_products = self.filtered(lambda l: l.product_id.type in ['product', 'consu'])
            if line_products.mapped('qty_delivered') and float_compare(values['product_uom_qty'],
                                                                       max(line_products.mapped('qty_delivered')),
                                                                       precision_digits=precision) == -1:
                raise UserError(_('You cannot decrease the ordered quantity below the delivered quantity.\n'
                                  'Create a return first.'))
            msg += "</ul>"

            order.message_post(body=msg)
