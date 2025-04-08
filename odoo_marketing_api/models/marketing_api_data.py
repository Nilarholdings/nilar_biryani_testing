from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PaymentTerms(models.Model):
    _inherit = 'pos.payment.method'
    marketing_payment = fields.Boolean(string="Marketing Payment")


class MarketingPricelist(models.Model):
    _inherit = 'product.pricelist'
    marketing_pricelist = fields.Boolean(string="Marketing Pricelist")


class SaleTeam(models.Model):
    _inherit = 'crm.team'
    marketing_sale = fields.Boolean(string="Marketing Sale")


class PaymentTerms(models.Model):
    _inherit = 'account.payment.term'
    marketing_payment_term = fields.Boolean(string="Marketing Payment")

class ProductTaxs(models.Model):
    _inherit = 'account.tax'
    marketing_tax = fields.Boolean(string="Tax for Marketing")

class AnalytiAccount(models.Model):
    _inherit = 'account.analytic.account'
    marketing_account = fields.Boolean(string="Account For Marketing")


# class MobilePayment(models.Model):
#     _inherit = 'sale.order'
#     mobile_payment = fields.Many2one('pos.payment.method', 'Mobile Payment')
#
# class MobilePaymentRegister(models.Model):
#     _inherit = 'account.move'
#     mobile_payment_id = fields.Many2one('pos.payment.method', readonly=True, tracking=True,
#         states={'draft': [('readonly', False)]},
#
#         string='Mobile Payment')


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    payment_method_id = fields.Many2one('pos.payment.method', string="Mobile Payment Method")

class AccountMove(models.Model):
    _inherit = 'account.move'
    # Create a Many2one field in account.move to link to payment_method_id in sale.order
    mobile_payment_method_id = fields.Many2one(
        'pos.payment.method',  # The related model
        string='Mobile Payment Method',  # Label for the field
        store=True,  # Store the field value for easier querying
        # readonly=True,  # Make the field readonly to prevent direct modification
    )

    @api.model
    def create(self, vals):
        # Automatically set the mobile_payment_method_id from sale.order's payment_method_id
        if vals.get('invoice_origin'):
            sale_order = self.env['sale.order'].search([('name', '=', vals['invoice_origin'])], limit=1)
            if sale_order:
                vals['mobile_payment_method_id'] = sale_order.payment_method_id.id
        return super(AccountMove, self).create(vals)

class MarketingLocation(models.Model):
    _inherit = 'stock.location'
    marketing_location = fields.Boolean(string="Marketing Location")