from odoo import models, fields, api, _
from odoo.http import request


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    inventory_product_tab_access = fields.Boolean('Access Inventory Tab', default=True
                                                  )
    accounting_product_tab_access = fields.Boolean('Access Accounting', default=True
                                                   )
    variants_access = fields.Boolean('Access Variants Tab', default=True)

    extra_price_access = fields.Boolean('Access Extra Prices', default=False)
    inventory_packaging_access = fields.Boolean('Access Packaging', default=False)
    in_out_access = fields.Boolean('Access In Out', default=False)
    lot_access = fields.Boolean('Access Lot', default=False)
    putaway_access = fields.Boolean('Access Putaway Rules', default=False)
    packing_sold_access = fields.Boolean('Access Sold', default=False)
    storage_categ_access = fields.Boolean('Access Storage Capacities', default=False)

    # @api.depends('company_id')
    # def compute_hide_tab(self):
    #     for rec in self:
    #         if self.user_has_groups('user_access_right.group_inventory_tab') and rec.type != 'service':
    #             rec.inventory_product_tab_access = True
    #         else:
    #             rec.inventory_product_tab_access = False
    #
    #         if self.user_has_groups('user_access_right.group_product_accounting_tab'):
    #             rec.accounting_product_tab_access = True
    #         else:
    #             rec.accounting_product_tab_access = False
    #
    #         if self.user_has_groups('user_access_right.group_product_variants_tab'):
    #             rec.variants_access = True
    #         else:
    #             rec.variants_access = False
    #
    #         if self.user_has_groups('user_access_right.group_inventory_packaging') and (rec.type in ['product',
    #                                                                                                  'consu'] or rec.product_variant_count <= 1 or rec.is_product_variant == True):
    #             rec.inventory_packaging_access = True
    #         else:
    #             rec.inventory_packaging_access = False
    #
    #         if self.user_has_groups('user_access_right.group_product_extra_price'):
    #             rec.extra_price_access = True
    #         else:
    #             rec.extra_price_access = False
    #
    #         if self.user_has_groups('user_access_right.group_product_in_out') and rec.type in ['product', 'consu']:
    #             rec.in_out_access = True
    #         else:
    #             rec.in_out_access = False
    #
    #         if self.user_has_groups('user_access_right.group_product_lot') and rec.tracking != 'none':
    #             rec.lot_access = True
    #         else:
    #             rec.lot_access = False
    #
    #         if self.user_has_groups('user_access_right.group_product_lot') and rec.type != 'service':
    #             rec.putaway_access = True
    #         else:
    #             rec.putaway_access = False
    #
    #         if self.user_has_groups('user_access_right.group_storage_categ') and rec.type == 'service':
    #             rec.storage_categ_access = True
    #         else:
    #             rec.storage_categ_access = False
    #
    #         if self.user_has_groups('user_access_right.group_product_sold') and rec.sale_ok:
    #             rec.packing_sold_access = True
    #         else:
    #             rec.packing_sold_access = False
