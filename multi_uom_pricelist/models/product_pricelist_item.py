from odoo import api, models, fields, _
from odoo.exceptions import UserError


# within multi uom of pricelist
class PricelistItemUom(models.Model):
    _inherit = 'pricelist.item.uom'

    @api.model
    def create(self, values):
        pricelist = super(PricelistItemUom, self).create(values)
        if 'product_id' in values:
            self.env['product.pricelist.item'].create({
                'product_tmpl_id': self.env['product.product'].browse(values['product_id']).product_tmpl_id.id,
                'product_id': values['product_id'],
                'min_quantity': values['pricelist_qty'] if 'pricelsit_qty' in values else 0,
                'fixed_price': values['price'] if 'price' in values else 0,
                'pricelist_id': values['pricelist_id'] if 'pricelist_id' in values else 0,
                'product_pricelist_item_id': pricelist.id,
            })
        return pricelist

    @api.model
    def write(self, values):
        pricelist = super(PricelistItemUom, self).write(values)
        if 'product_id' in values or 'pricelsit_qty' in values or 'price' in values:
            line = self.env['product.pricelist.item'].search(
                [('product_pricelist_item_id', '=', self.id), ('pricelist_id', '=', self.pricelist_id.id)], limit=1)
            if line:
                line.write({
                    'product_tmpl_id': self.env['product.product'].browse(values[
                                                                              'product_id']).product_tmpl_id.id if 'product_id' in values else self.product_id.product_tmpl_id.id,
                    'product_id': values['product_id'] if 'product_id' in values else self.product_id.id,
                    'min_quantity': values['pricelist_qty'] if 'pricelsit_qty' in values else self.pricelist_qty,
                    'fixed_price': values['price'] if 'price' in values else self.price,
                })
            else:
                raise UserError(_("Please Run with Server Action and add pricelist!!"))


class PricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    product_pricelist_item_id = fields.Many2one('pricelist.item.uom', 'Multi Uom Pricelist', ondelete='cascade')
