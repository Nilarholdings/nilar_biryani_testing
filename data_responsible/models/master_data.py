from odoo import models, fields, api, _

class ProductCategory(models.Model):
    _inherit = 'product.category'

    responsible_id = fields.Many2one('data.responsible','Responsible')
    is_used = fields.Boolean("Is used?",compute="compute_is_used")
    # x_selling_category = fields.Boolean(string='Selling Category')

    def compute_is_used(self):
        product_categ_ids = self.env['product.template'].search([]).categ_id.ids
        for rec in self:
            if rec.id in product_categ_ids:
                rec.is_used = True
            else:
                rec.is_used = False

class POSProductCategory(models.Model):
    _inherit = 'pos.category'

    responsible_id = fields.Many2one('data.responsible','Responsible')
    is_used = fields.Boolean("Is used?",compute="compute_is_used")

    def compute_is_used(self):
        pos_categ_ids = self.env['product.template'].search([]).pos_categ_id.ids
        for rec in self:
            if rec.id in pos_categ_ids:
                rec.is_used = True
            else:
                rec.is_used = False

class ProductFamily(models.Model):
    _inherit = 'product.family'

    responsible_id = fields.Many2one('data.responsible','Responsible')
    is_used = fields.Boolean("Is used?",compute="compute_is_used")

    def compute_is_used(self):
        product_family_ids = self.env['product.template'].search([]).product_family_id.ids
        for rec in self:
            if rec.id in product_family_ids:
                rec.is_used = True
            else:
                rec.is_used = False

class ProductGroup(models.Model):
    _inherit = 'product.group'

    responsible_id = fields.Many2one('data.responsible','Responsible')
    is_used = fields.Boolean("Is used?",compute="compute_is_used")

    def compute_is_used(self):
        product_group_ids = self.env['product.template'].search([]).product_group_id.ids
        for rec in self:
            if rec.id in product_group_ids:
                rec.is_used = True
            else:
                rec.is_used = False

class ProductBrand(models.Model):
    _inherit = 'product.brand'

    responsible_id = fields.Many2one('data.responsible','Responsible')
    is_used = fields.Boolean("Is used?",compute="compute_is_used")

    def compute_is_used(self):
        brand_ids = self.env['product.template'].search([]).brand_id.ids
        for rec in self:
            if rec.id in brand_ids:
                rec.is_used = True
            else:
                rec.is_used = False


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    responsible = fields.Char('Responsible')
    code = fields.Char('Short Name', required=True, size=10, help="Short name used to identify your warehouse")
