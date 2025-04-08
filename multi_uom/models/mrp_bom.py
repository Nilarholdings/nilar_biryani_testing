from odoo import api, models, fields, _


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    multi_uom_line_ids = fields.Many2many('multi.uom.line', compute='compute_multi_uom_line_ids')
    multi_uom_line_id = fields.Many2one('multi.uom.line', 'Multi UOM')
    multi_uom_code = fields.Char('Multi UOM Text')
    product_multi_uom_qty = fields.Float('Multi Request Qty', default=1.0,
                                         digits='Product Unit of Measure', required=True, tracking=2)

    @api.model
    def create(self, values):
        uom = []
        product_id = values['product_tmpl_id']
        if 'multi_uom_code'in values:
            uom = self.env['multi.uom.line'].search([('uom_code', '=', values['multi_uom_code']), ('product_tmpl_id', '=', product_id)], limit=1)
            values.update({
                'multi_uom_line_id': uom.id
            })
            product_uom_id = uom.uom_id.id
        else:
            uom_id = values['multi_uom_line_id']
            uom_line_id = self.env['multi.uom.line'].browse(uom_id)
            product = self.env['product.template'].browse(product_id)
            multi_uom_line_id = product.multi_uom_line_ids.filtered(lambda l: l.uom_id.id == uom_line_id.uom_id.id and l.product_tmpl_id.id == product_id)
            product_uom_id = multi_uom_line_id.uom_id.id
        if 'product_uom_id' not in values:
            values.update({
                'product_uom_id': product_uom_id
            })
        return super(MrpBom, self).create(values)

    @api.depends('product_tmpl_id')
    def compute_multi_uom_line_ids(self):
        for rec in self:
            rec.multi_uom_line_ids = []
            if rec.product_tmpl_id.multi_uom_line_ids:
                rec.multi_uom_line_ids = rec.product_tmpl_id.multi_uom_line_ids.ids

    @api.onchange('product_tmpl_id')
    def product_id_change(self):
        for rec in self:
            if rec.product_tmpl_id:
                line = rec.product_tmpl_id.multi_uom_line_ids.filtered(lambda l: l.is_default_uom == True)
                rec.multi_uom_line_id = line

    @api.onchange('product_tmpl_id', 'multi_uom_line_id')
    def _change_multi_uom_qty(self):
        for rec in self:
            if rec.product_id and rec.product_multi_uom_qty and rec.multi_uom_line_id:
                rec.product_qty = rec.multi_uom_line_id.ratio * rec.product_multi_uom_qty


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    multi_uom_line_ids = fields.Many2many('multi.uom.line', compute='compute_multi_uom_line_ids')
    multi_uom_line_id = fields.Many2one('multi.uom.line', 'Multi UOM')
    product_multi_uom_qty = fields.Float('Multi Request Qty', default=1.0,
                                         digits='Product Unit of Measure')
    real_product_qty = fields.Float(string='Real Product Qty', compute='compute_real_product_qty')
    product_qty = fields.Float(compute='compute_product_uom_qty',
                               inverse='set_multi_uom_qty',
                               store=True,
                               readonly=False)

    @api.depends('multi_uom_line_id', 'product_multi_uom_qty')
    def compute_product_uom_qty(self):
        for rec in self:
            if rec.multi_uom_line_id:
                rec.product_qty = rec.product_multi_uom_qty * rec.multi_uom_line_id.ratio
                # print(rec.product_multi_uom_qty, rec.multi_uom_line_id.ratio, '22222222222222222222222222222')
            else:
                rec.product_qty = 0

    def set_multi_uom_qty(self):
        for rec in self:
            if rec.multi_uom_line_id:
                rec.product_multi_uom_qty = rec.product_qty / rec.multi_uom_line_id.ratio
            else:
                rec.product_multi_uom_qty = rec.product_qty
                # print(rec.product_qty, rec.multi_uom_line_id.ratio, '1111111111111111111111111111111111111')

    @api.model
    def create(self, values):

        product_id = values['product_id']
        product = self.env['product.product'].browse(product_id)

        if product.multi_uom_line_ids and values['bom_id']:
            uom_id = values['multi_uom_line_id']
            uom_line_id = self.env['multi.uom.line'].browse(uom_id)
            multi_uom_line_id = product.multi_uom_line_ids.filtered(lambda l: l.uom_id.id == uom_line_id.uom_id.id)
            if 'product_qty' not in values:
                product_qty = values['product_multi_uom_qty'] * multi_uom_line_id.ratio
                values.update({
                    'product_qty': product_qty
                })
            values.update({
                'multi_uom_line_id': multi_uom_line_id.id
            })

        # print(multi_uom_line_id.uom_id.name, '222222222222222222222222222222', uom_line_id.uom_id.name)
        return super(MrpBomLine, self).create(values)

    @api.depends('product_multi_uom_qty')
    def compute_real_product_qty(self):
        self.real_product_qty = 0.0
        for rec in self:
            if rec.product_multi_uom_qty:
                rec.real_product_qty = rec.product_multi_uom_qty

    @api.depends('product_id')
    def compute_multi_uom_line_ids(self):
        for rec in self:
            rec.multi_uom_line_ids = []
            if rec.product_id.multi_uom_line_ids:
                rec.multi_uom_line_ids = rec.product_id.multi_uom_line_ids.ids

    @api.onchange('product_id')
    def product_id_change(self):
        for rec in self:
            if rec.product_id:
                line = rec.product_id.multi_uom_line_ids.filtered(lambda l: l.is_default_uom == True)
                rec.multi_uom_line_id = line

    @api.onchange('product_multi_uom_qty', 'product_id', 'multi_uom_line_id')
    def _change_multi_uom_qty(self):
        for rec in self:

            if rec.product_id and rec.product_multi_uom_qty and rec.multi_uom_line_id:
                rec.product_qty = rec.multi_uom_line_id.ratio * rec.product_multi_uom_qty
                rec.product_uom_id = rec.product_id.uom_id.id


class MrpBomByProduct(models.Model):
    _inherit = "mrp.bom.byproduct"

    multi_uom_line_ids = fields.Many2many('multi.uom.line', compute='compute_multi_uom_line_ids')
    multi_uom_line_id = fields.Many2one('multi.uom.line', 'Multi UOM')
    product_multi_uom_qty = fields.Float('Multi Request Qty', default=1.0,
                                         digits='Product Unit of Measure')

    @api.depends('product_id')
    def compute_multi_uom_line_ids(self):
        for rec in self:
            rec.multi_uom_line_ids = []
            if rec.product_id.multi_uom_line_ids:
                rec.multi_uom_line_ids = rec.product_id.multi_uom_line_ids.ids

    @api.onchange('product_id')
    def product_id_change(self):
        for rec in self:
            if rec.product_id:
                line = rec.product_id.multi_uom_line_ids.filtered(lambda l: l.is_default_uom == True)
                rec.multi_uom_line_id = line

    @api.onchange('product_multi_uom_qty', 'product_id', 'multi_uom_line_id')
    def _change_multi_uom_qty(self):
        for rec in self:
            if rec.product_id and rec.product_multi_uom_qty and rec.multi_uom_line_id:
                rec.product_qty = rec.multi_uom_line_id.ratio * rec.product_multi_uom_qty
