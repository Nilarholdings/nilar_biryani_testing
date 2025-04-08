from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'
    x_is_a_mobile = fields.Boolean(string="Is a Mobile")#to delete


    @api.constrains('phone')
    def _check_unique_phone_for_mobile_customers(self):
        for partner in self:
            if partner.phone:
                duplicate = self.search([
                    ('phone', '=', partner.phone),
                    ('id', '!=', partner.id),
                    # ('x_is_a_mobile', '=', True),
                    # ('customer', '=', True)
                ])
                if duplicate:
                    raise ValidationError(
                        "The phone number  is already exited."
                    )
                else:
                    pass



class ProductCategory(models.Model):
    _inherit = 'product.category'
    x_selling_category = fields.Boolean(string='Selling Category')

class ResCountry(models.Model):
    _inherit = 'res.country'
    default_country = fields.Boolean(string="Default Country")

class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'
    mobile_pricelist = fields.Boolean(string="Mobile Pricelist")

class ProductTaxs(models.Model):
    _inherit = 'account.tax'
    mobile_tax = fields.Boolean(string="Tax for Mobile")

class SaleTeam(models.Model):
    _inherit = 'crm.team'
    mobile_sale = fields.Boolean(string="Mobile Sale")

class PaymentTerms(models.Model):
    _inherit = 'account.payment.term'
    mobile_payment_term = fields.Boolean(string="Mobile Payment")