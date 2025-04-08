# -*- coding: utf-8 -*-
import json
import math
import logging
import requests
import re

from odoo import http, _, exceptions
from odoo.http import request
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta



from odoo.http import request
from odoo import http, tools

from PIL import Image
from io import BytesIO
import base64




_logger = logging.getLogger(__name__)

def error_response(error, msg):
    return {
        "jsonrpc": "2.0",
        "id": None,
        "error": {
            "code": 200,
            "message": msg,
            "data": {
                "name": str(error),
                "debug": "",
                "message": msg,
                "arguments": list(error.args),
                "exception_type": type(error).__name__
            }
        }
    }


class OdooAPI(http.Controller):
    # success login
    @http.route('/api/login', type='json', auth='none', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        # Your code here
        return {'status': 'login success for marketing'}
    # for authenticate
    # @http.route('/auth/', type='json', auth='user', methods=["POST"], csrf=False)
    # def authenticate(self, *args, **post):
    #     try:
    #         login = post["login"]
    #     except KeyError:
    #         raise exceptions.AccessDenied(message='`login` is required.')
    #     try:
    #         password = post["password"]
    #     except KeyError:
    #         raise exceptions.AccessDenied(message='`password` is required.')
    #     try:
    #         db = post["db"]
    #     except KeyError:
    #         raise exceptions.AccessDenied(message='`db` is required.')
    #     http.request.session.authenticate(db, login, password)
    #     res = request.env['ir.http'].session_info()
    #     return res

    @http.route(
        '/auth/',
        type='json', auth='none', methods=["POST"], csrf=False)
    def authenticate(self, *args, **post):
        try:
            login = post["login"]
        except KeyError:
            raise exceptions.AccessDenied(message='`login` is required.')
        try:
            password = post["password"]
        except KeyError:
            raise exceptions.AccessDenied(message='`password` is required.')
        try:
            db = post["db"]
        except KeyError:
            raise exceptions.AccessDenied(message='`db` is required.')
        http.request.session.authenticate(db, login, password)
        res = request.env['ir.http'].session_info()
        return res

    @http.route('/api/pos/categories', type='json', auth='user', methods=['POST'], csrf=False)
    def get_pos_categories(self, **kwargs):
        """
        Fetch all POS categories.
        """
        categories = request.env['pos.category'].sudo().search([])
        data = [{'id': cat.id, 'name': cat.name, 'parent_id': cat.parent_id.id, 'is_used': cat.is_used} for cat in categories]
        return {'status': 'success', 'data': data}

    @http.route('/api/pos/products_by_category', type='json', auth='user', methods=['POST'])
    def get_products_by_pos_category(self):
        """
        Retrieve products available in POS for a specific POS category, including their stock quantities.
        """
        # Retrieve data from the request payload
        data = request.jsonrequest
        pos_category_id = data.get('pos_category_id')

        # Validate pos_category_id
        if not pos_category_id:
            return {"error": "POS Category ID is required"}

        # Check if the POS category exists
        pos_category = request.env['pos.category'].sudo().browse(pos_category_id)
        if not pos_category.exists():
            return {"error": f"POS Category with ID {pos_category_id} does not exist"}

        # Fetch products belonging to the POS category
        products = request.env['product.product'].sudo().search([
            ('pos_categ_id', '=', pos_category.id),  # Filter by POS category
            ('available_in_pos', '=', True),  # Only products available in POS
            ('qty_available', '>', 0)  # Only products with stock > 0
        ])

        # Prepare the product data
        product_data = [{
            'id': product.id,
            'name': product.name,
            'code': product.default_code,
            'qty_available': product.qty_available,
            'list_price': product.list_price,
            'image': product.image_1920 and product.image_1920.decode('utf-8') or ''
        } for product in products]

        # Prepare the response
        response_data = {
            'pos_category_id': pos_category.id,
            'pos_category_name': pos_category.name,
            'products': product_data,
        }

        return response_data

    @http.route('/api/location/product/pos_category', type='json', auth='user', methods=['POST'])
    def get_location_product_pos_category(self):
        """
        Retrieve POS details for a specific location, including products and on-hand quantities,
        filtered by selling category.
        """
        # Retrieve location_id from the JSON payload
        location_id = request.jsonrequest.get('location_id')
        if not location_id:
            return {"error": "Location ID is required"}

        # Check if the location exists
        location = request.env['stock.location'].sudo().browse(location_id)
        if not location.exists():
            return {"error": f"Location with ID {location_id} does not exist"}

        # Fetch products and on-hand quantities for the location
        stock_quants = request.env['stock.quant'].sudo().search([
            ('location_id', '=', location.id),
            ('product_id.available_in_pos', '=', True),
            ('quantity', '>', 0)  # Only include products with stock
        ])

        # Prepare the product data
        products = [{
            'id': quant.product_id.product_tmpl_id.id,
            'name': quant.product_id.product_tmpl_id.name,
            'code': quant.product_id.default_code,
            'qty_available': quant.quantity,
            'list_price': quant.product_id.product_tmpl_id.list_price,
            'image': quant.product_id.image_1920 and quant.product_id.image_1920.decode('utf-8') or '',
            'pos_categ_id': quant.product_id.product_tmpl_id.pos_categ_id.id,  # Add pos_categ_id here
            'pos_categ_name': quant.product_id.product_tmpl_id.pos_categ_id.name  # Add pos_categ_name here
        } for quant in stock_quants]

        # Prepare the response
        response_data = {
            'location_id': location.id,
            'location_name': location.display_name,
            'products': products,
        }

        return response_data

    # @http.route('/api/cancel/draft/sale_order', type='json', auth='user', methods=['POST'], csrf=False)
    # def cancel_draft_sale_order(self, **kwargs):
    #     """
    #     Cancel a sale order only if it's in the draft state.
    #     """
    #     # Get the sale_order_id from the request
    #     sale_order_id = kwargs.get('sale_order_id')
    #     if not sale_order_id:
    #         return {
    #             'success': False,
    #             'error': 'Missing sale_order_id in the request.'
    #         }
    #
    #     # Fetch the sale order record
    #     sale_order = request.env['sale.order'].sudo().browse(sale_order_id)
    #     if not sale_order.exists():
    #         return {
    #             'success': False,
    #             'error': f'Sale order with ID {sale_order_id} not found.'
    #         }
    #
    #     # Check if the sale order is in draft state
    #     if sale_order.state != 'draft':
    #         return {
    #             'success': False,
    #             'error': f'Sale order {sale_order.name} is not in draft state. Current state: {sale_order.state}.'
    #         }
    #
    #     try:
    #         # Perform the cancellation
    #         sale_order.sudo().action_cancel()
    #
    #         return {
    #             'success': True,
    #             'message': f'Sale order {sale_order.name} has been canceled successfully.'
    #         }
    #
    #     except Exception as e:
    #         return {
    #             'success': False,
    #             'error': f'Error while canceling sale order: {str(e)}'
    #         }

    @http.route('/api/marketing/payment_term', type='json', auth='user', methods=["POST"], csrf=False)
    def get_payment_term(self, **post):
        domain = []
        # Perform search_read on the 'res.country' model
        payment_term = request.env['account.payment.term'].search_read(domain,fields=['id', 'name'],)
        # Return the countries data in JSON format
        return payment_term

    @http.route('/api/marketing/sale_team', type='json', auth='user', methods=["POST"], csrf=False)
    def get_sale_team(self, **post):
        domain = []
        # Perform search_read on the 'res.country' model
        sale_team = request.env['crm.team'].search_read(domain,fields=['id', 'name'],)
        # Return the countries data in JSON format
        return sale_team

    @http.route('/api/marketing/pricelist', type='json', auth='user', methods=["POST"], csrf=False)
    def get_pricelist(self, **post):
        domain = []
        # Perform search_read on the 'product.pricelist' model
        pricelist = request.env['product.pricelist'].search_read(domain,
                                                                 fields=['id', 'name'],
                                                                 )
        # Return the countries data in JSON format
        return pricelist

    # @http.route('/api/create/marketing_sale_orders', type='json', auth='none', methods=['POST'], csrf=False)
    # def create_marketing_sale_order(self, **kwargs):
    #     params = request.jsonrequest
    #     uid = request.session.uid
    #     if not uid:
    #         return {'success': False, 'error': 'Invalid cookie.'}
    #     company_id = request.env['res.users'].sudo().browse(uid).company_id.id
    #
    #     # Fetch the company's short code
    #     company = request.env['res.company'].sudo().browse(company_id)
    #     company_short_code = company.short_code or "N/A"
    #
    #     # Get the analytic account id from params
    #     analytic_account_id = params.get('analytic_account_id', False)
    #     warehouse_id = False
    #     short_code = None
    #
    #     if analytic_account_id:
    #         # Get the analytic account and associated warehouse
    #         analytic_account = request.env['account.analytic.account'].sudo().browse(analytic_account_id)
    #         if analytic_account.exists():
    #             warehouse_id = analytic_account.location_id and analytic_account.location_id.warehouse_id.id
    #             short_code = analytic_account.short_code
    #
    #     if not warehouse_id:
    #         return {'success': False, 'error': 'No warehouse found for the selected analytic account.'}
    #
    #     # Fetch Shop Details
    #     to_shop_id = params.get('to_shop_id', False)
    #     to_shop_name = to_shop_ph = False
    #     if to_shop_id:
    #         shop = request.env['shop.to.take'].sudo().browse(to_shop_id)
    #         if shop.exists():
    #             to_shop_name = shop.name
    #             to_shop_ph = shop.phone
    #
    #     # Fetch pricelist
    #     pricelist_id = params.get('pricelist_id', False)  # Getting pricelist_id from the params
    #     if not pricelist_id:
    #         return {'success': False, 'error': 'Pricelist ID is required.'}
    #     pricelist = request.env['product.pricelist'].sudo().browse(pricelist_id)
    #     if not pricelist.exists():
    #         return {'success': False, 'error': 'Pricelist not found.'}
    #
    #     # # Fetch mobile sales teams
    #     # mobile_sales_teams = request.env['crm.team'].sudo().search([('mobile_sale', '=', True)], limit=1)
    #     # sale_team_id = mobile_sales_teams.id
    #
    #     # Fetch mobile payment terms
    #     mobile_payment_terms = request.env['account.payment.term'].sudo().search([('mobile_payment_term', '=', True)],
    #                                                                              limit=1)
    #     payment_term_id = mobile_payment_terms.id
    #
    #     # Prepare Sale Order Values
    #     values = {
    #         'partner_id': params.get('partner_id', False),
    #         'partner_invoice_id': params.get('partner_invoice_id', False),
    #         'partner_shipping_id': params.get('partner_shipping_id', False),
    #         'date_order': params.get('date_order', False),
    #         'pricelist_id': pricelist.id,  # Use pricelist from the request
    #         'currency_id': params.get('currency_id', False),
    #         'payment_term_id': payment_term_id,
    #         'analytic_account_id': analytic_account_id,
    #         'warehouse_id': warehouse_id,
    #         'user_id': params.get('user_id', False),
    #         'sale_picking': params.get('sale_picking', False),
    #         'company_id': company_id,
    #         'commitment_date': params.get('commitment_date', False),
    #         'contact_ph': params.get('contact_ph', False),
    #         'to_shop_name': to_shop_name,
    #         'to_shop_ph': to_shop_ph,
    #         'team_id': params.get('team_id', False),
    #         'actual_start_time': params.get('actual_start_time', False),
    #     }
    #
    #     available_fields = request.env['sale.order'].fields_get_keys()
    #     for field in params:
    #         if field in available_fields:
    #             values[field] = params[field]
    #
    #     # # Fetch taxes
    #     # account_taxes = request.env['account.tax'].sudo().search([('mobile_tax', '=', True)])
    #
    #     # Create sale order lines
    #     order_lines = []
    #     for product in params.get('products', []):
    #         product_record = request.env['product.product'].sudo().search(
    #             [('product_tmpl_id', '=', product['product_id'])])
    #         if not product_record.exists():
    #             return {'success': False, 'error': f'Product with ID {product["product_id"]} not found.'}
    #
    #         default_uom_line = product_record.multi_uom_line_ids.filtered(lambda u: u.is_default_uom)
    #         if not default_uom_line:
    #             return {'success': False, 'error': f'Default UOM not set for product {product_record.name}.'}
    #
    #         uom_ratio = default_uom_line.ratio
    #         product_qty = product['qty'] * uom_ratio
    #         product_discount = product.get('discount', 0)
    #
    #         # Use the provided pricelist to fetch the price
    #         product_price_unit = pricelist.with_context(company_id=company_id)._get_pricelist_uom_price(
    #             product_record, default_uom_line, product_qty)
    #
    #         total_price = product_qty * product_price_unit * (1 - product_discount / 100)
    #         line_vals = {
    #             'product_id': product_record.id,
    #             'product_uom_qty': product_qty,
    #             'price_unit': product_price_unit,
    #             'discount': product_discount,
    #             'multi_uom_line_id': default_uom_line.id,
    #             'product_uom': default_uom_line.uom_id.id,
    #             'name': product.get('description', product_record.name),
    #             'price_total': total_price,
    #
    #         }
    #         order_lines.append((0, 0, line_vals))
    #
    #     values['order_line'] = order_lines
    #
    #     # Create the sale order
    #     order = request.env['sale.order'].sudo().create(values)
    #     order_name = f'{company_short_code}/SO/{short_code}/{datetime.now().strftime("%y/%m")}/{str(order.id)}'
    #     order.write({"name": order_name})
    #
    #     # Skip tax computation
    #     # Remove any tax computation if you want to ensure no tax calculation happens
    #     order.order_line.write({'tax_id': [(5, 0, 0)]})  # Unsets any taxes on the order lines
    #
    #     return {
    #         'success': True,
    #         'order_id': order.id,
    #         'name': order.name,
    #
    #     }

    @http.route('/api/cancel/marketing_sale_order', type='json', auth='user', methods=['POST'], csrf=False)
    def cancel_marketing_sale_order(self, **kwargs):
        """
        Cancel a sale order, regardless of its state.
        """
        sale_order_id = request.jsonrequest.get('sale_order_id')
        # Get the sale_order_id from the request

        if not sale_order_id:
            return {
                'success': False,
                'error': 'Missing sale_order_id in the request.'
            }

        # Fetch the sale order record
        sale_order = request.env['sale.order'].sudo().browse(sale_order_id)
        if not sale_order.exists():
            return {
                'success': False,
                'error': f'Sale order with ID {sale_order_id} not found.'
            }

        try:
            # Handle cancellation for all states
            if sale_order.state in ['sale', 'done']:
                # Unlink related deliveries
                if sale_order.picking_ids:
                    sale_order.picking_ids.sudo().action_cancel()

                # Cancel related invoices
                if sale_order.invoice_ids:
                    for invoice in sale_order.invoice_ids:
                        if invoice.state not in ['draft', 'cancel']:
                            invoice.sudo().action_invoice_cancel()

            # Perform the cancellation
            sale_order.sudo().action_cancel()

            return {
                'success': True,
                'message': f'Sale order {sale_order.name} has been canceled successfully.'
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error while canceling sale order: {str(e)}'
            }

    @http.route('/api/marketing/sale_order_history', type='json', auth='user')
    def get_sale_orders_history(self, customer_id=None):
        data = request.jsonrequest
        user_id = data.get('user_id')
        if not user_id:
            return {'error': 'User ID is required'}

        # Fetch sales teams where 'mobile_sale = True'
        marketing_sales_teams = request.env['crm.team'].sudo().search([('marketing_sale', '=', True)])
        if not marketing_sales_teams:
            return {'error': 'No mobile sales teams found'}

        # Use the first mobile sales team
        sale_team_id = marketing_sales_teams[0].id

        # Fetch sale orders for the given customer
        sale_orders = request.env['sale.order'].search([
            ('user_id', '=', int(user_id)),
            ('team_id', '=', sale_team_id),  # Filter by sales team

        ])

        if not sale_orders:
            return {'error': 'No sale orders found for the given customer'}

        result = []
        for order in sale_orders:

            order_data = {
                "orderid": order.id,
                "customer_name": order.partner_id.name or "",
                "date_order": order.date_order or "",
                "total_qty": sum(line.product_uom_qty for line in order.order_line),
                "untaxed_amount": order.amount_untaxed,
                "taxes": order.amount_tax,  # Detailed tax breakdown
                "total_price": order.amount_total,
                "shop_name": order.warehouse_id.name or "",
                'state': order.state,

                'order_lines': []
            }
            for line in order.order_line:
                # Add line details including price and taxes
                order_data['order_lines'].append({
                    'line_id': line.id,
                    'product_id': line.product_id.id,
                    'product_name': line.product_id.name,
                    'quantity': line.multi_uom_qty,
                    'price_unit': line.multi_price_unit,
                    'price_total': line.price_total,  # Without taxes
                })
            result.append(order_data)

        return result

    @http.route('/api/marketing/payment', type='json', auth='user', methods=["POST"], csrf=False)
    def get_marketing_payment(self, **post):
        domain = [('marketing_payment', '=', True)]

        # Perform search_read on the 'res.partner' model
        customers = request.env['pos.payment.method'].search_read(
            domain,
            fields=[ 'id','name', 'journal_id'],
        )
        return customers

    # @http.route('/api/marketing/create/sale-orders', type='json', auth='none', methods=['POST'], csrf=False)
    # def create_marketing_sale_order(self, **kwargs):
    #     params = request.jsonrequest
    #     uid = request.session.uid
    #     if not uid:
    #         return {'success': False, 'error': 'Invalid cookie.'}
    #
    #     company_id = request.env['res.users'].sudo().browse(uid).company_id.id
    #
    #     # Fetch the company's short code
    #     company = request.env['res.company'].sudo().browse(company_id)
    #     company_short_code = company.short_code or "N/A"
    #
    #     # Get the analytic account id from params
    #     analytic_account_id = params.get('analytic_account_id', False)
    #     warehouse_id = False
    #     short_code = None
    #
    #     # branch = self.env['res.company'].browse('company_id')
    #     # branch_code = branch.short_code
    #
    #     if analytic_account_id:
    #         # Get the analytic account and associated warehouse
    #         analytic_account = request.env['account.analytic.account'].sudo().browse(analytic_account_id)
    #         if analytic_account.exists():
    #             # If an analytic account exists, fetch the related warehouse using location_id
    #             warehouse_id = analytic_account.location_id and analytic_account.location_id.warehouse_id.id
    #             short_code= analytic_account.short_code  # Access the shot_code field
    #
    #     # If no warehouse_id was found, return an error
    #     if not warehouse_id:
    #         return {'success': False, 'error': 'No warehouse found for the selected analytic account.'}
    #
    #     # Fetch Shop Details from shop.to.take model
    #     to_shop_id = params.get('to_shop_id', False)  # Assuming 'to_shop_id' is passed in params
    #     to_shop_name = False
    #     to_shop_ph = False
    #     if to_shop_id:
    #         shop = request.env['shop.to.take'].sudo().browse(to_shop_id)
    #         if shop.exists():
    #             to_shop_name = shop.name  # Assuming 'name' field in 'shop.to.take' stores the shop name
    #             to_shop_ph = shop.phone  # Assuming 'phone' field in 'shop.to.take' stores the shop phone
    #
    #     # Fetch the company-specific pricelist
    #     pricelist = request.env['product.pricelist'].sudo().search(
    #         [('marketing_pricelist', '=', True)], limit=1
    #     )
    #
    #     # Fetch sales teams where 'mobile_sale = True'
    #     marketing_sales_teams = request.env['crm.team'].sudo().search([('marketing_sale', '=', True)])
    #     # Use the first mobile sales team (or logic to determine a specific one)
    #     sale_team_id = marketing_sales_teams.id
    #
    #     # Fetch payment terms where 'mobile_payment_term = True'
    #     mobile_payment_terms = request.env['account.payment.term'].sudo().search([('marketing_payment_term', '=', True)])
    #     payment_term_id = mobile_payment_terms.id
    #
    #     # Prepare Sale Order Values
    #     values = {
    #         'partner_id': params.get('partner_id', False),
    #         'partner_invoice_id': params.get('partner_invoice_id', False),
    #         'partner_shipping_id': params.get('partner_shipping_id', False),
    #         'date_order': params.get('date_order', False),
    #         'pricelist_id': pricelist.id,  # Use the fetched pricelist
    #         'currency_id': params.get('currency_id', False),
    #         'payment_term_id': payment_term_id,
    #         'analytic_account_id': analytic_account_id,  # Set analytic account ID
    #         'warehouse_id': warehouse_id,  # Set warehouse based on the analytic account
    #         'user_id': params.get('user_id', False),
    #         'sale_picking': params.get('sale_picking', False),
    #         'company_id': company_id,
    #         'commitment_date': params.get('commitment_date', False),
    #         'contact_ph': params.get('contact_ph', False),
    #         'to_shop_name': to_shop_name,  # Set the shop name
    #         'to_shop_ph': to_shop_ph,  # Set the shop phone
    #         'team_id': sale_team_id,
    #         'actual_start_time': params.get('actual_start_time', False),
    #         'payment_method_id': params.get('payment_method_id', False),
    #     }
    #
    #     # Get available fields for sale order and sale order lines
    #     available_fields = request.env['sale.order'].fields_get_keys()
    #     available_line_fields = request.env['sale.order.line'].fields_get_keys()
    #
    #     # Add additional fields from params to the sale order values
    #     for field in params:
    #         if field in available_fields:
    #             values[field] = params[field]
    #
    #     # Fetch taxes where mobile_tax is True
    #     account_taxes = request.env['account.tax'].sudo().search([('marketing_tax', '=', True)])
    #
    #     # Create sale order lines
    #     order_lines = []
    #     for product in params.get('products', []):
    #         # Fetch the product record
    #         product_record = request.env['product.product'].sudo().search(
    #             [('product_tmpl_id', '=', product['product_id'])])
    #         if not product_record.exists():
    #             return {'success': False, 'error': f'Product with ID {product["product_id"]} not found.'}
    #
    #
    #
    #         # Fetch default UOM from product.multi_uom_line_ids
    #         default_uom_line = product_record.multi_uom_line_ids.filtered(lambda u: u.is_default_uom)
    #         if not default_uom_line:
    #             return {'success': False, 'error': f'Default UOM not set for product {product_record.name}.'}
    #
    #         # Calculate UOM-based adjustments
    #         uom_ratio = default_uom_line.ratio
    #         # multi_uom_line = default_uom_line
    #
    #         # # Use list_price from product as the price_unit
    #         # product_price_unit = product_record.list_price / uom_ratio
    #
    #         # Calculate quantities and prices
    #         product_qty = product['qty'] * uom_ratio
    #         product_discount = product.get('discount', 0)
    #
    #         # Use the provided pricelist to fetch the price
    #         product_price_unit = pricelist.with_context(company_id=company_id)._get_pricelist_uom_price(
    #             product_record, default_uom_line, product_qty)
    #
    #         # Calculate total price
    #         total_price = product_qty * product_price_unit * (1 - product_discount / 100)
    #
    #         # Prepare the order line values
    #
    #         line_vals = {
    #             'product_id': product_record.id,
    #             'product_uom_qty': product_qty,  # Adjusted quantity
    #             'price_unit': product_price_unit,
    #             'discount': product_discount,  # Adjusted discount
    #             'multi_uom_line_id': default_uom_line.id,  # Default UOM
    #             'product_uom': default_uom_line.uom_id.id,  # Default UOM
    #             'name': product.get('description', product_record.name),  # Use provided description or product name
    #             'price_total': total_price,  # Total price for this line
    #             'tax_id': [(6, 0, account_taxes.ids)] if account_taxes else [(5, 0, 0)],
    #         }
    #
    #
    #         # Append to the order lines
    #         order_lines.append((0, 0, line_vals))
    #
    #     # Add the order lines to the sale order values
    #     values['order_line'] = order_lines
    #
    #     # Create the sale order
    #     order = request.env['sale.order'].sudo().create(values)
    #
    #     order_name = f'{company_short_code}/SO/{short_code}/{datetime.now().strftime("%y/%m")}/{str(order.id)}'
    #     order.write({
    #         "name": order_name
    #     })
    #
    #     # order.order_line.write({'tax_id': [(5, 0, 0)]})
    #
    #     order_data = {
    #         "orderid": order.id,
    #         "customer_name": order.partner_id.name or "",
    #         "date_time": order.date_order or "",
    #         "total_qty": sum(line.product_uom_qty for line in order.order_line),
    #         "untaxed_amount": order.amount_untaxed,
    #         "taxes": order.amount_tax,
    #         "total_price": order.amount_total,
    #         "shop_name": order.warehouse_id.name or "",
    #         'order_lines': []
    #     }
    #     for line in order.order_line:
    #         order_data['order_lines'].append({
    #             'line_id': line.id,
    #             'product_id': line.product_id.id,
    #             'product_name': line.product_id.name,
    #             'quantity': line.product_uom_qty,
    #             'price_unit': line.price_unit,
    #             'price_total': line.price_total,
    #         })
    #
    #     # Return success response
    #     return {
    #         'success': True,
    #         'order_id': order.id,
    #         'name': order.name,
    #         'warehouse_id': warehouse_id,
    #         'order_data': order_data
    #     }

    @http.route('/api/marketing/create/sale-orders', type='json', auth='none', methods=['POST'], csrf=False)
    def create_marketing_sale_order(self, **kwargs):
        params = request.jsonrequest
        uid = request.session.uid
        if not uid:
            return {'success': False, 'error': 'Invalid cookie.'}

        company_id = request.env['res.users'].sudo().browse(uid).company_id.id

        # Fetch the company's short code
        company = request.env['res.company'].sudo().browse(company_id)
        company_short_code = company.short_code or "N/A"

        # Fetch the salesperson ID (optional: default to the current user)
        salesperson_id = params.get('user_id', uid)

        # Get the analytic account id from params
        analytic_account = request.env['account.analytic.account'].sudo().search(
            [('marketing_account', '=', True)], limit=1
        )

        warehouse_id = False
        short_code = None

        if analytic_account:
            # Fetch the associated warehouse and short code
            warehouse_id = analytic_account.location_id.warehouse_id.id if analytic_account.location_id else False
            short_code = analytic_account.short_code

        # If no warehouse_id was found, return an error
        if not warehouse_id:
            return {'success': False, 'error': 'No warehouse found for the selected analytic account.'}

        # Fetch Shop Details from shop.to.take model
        to_shop_id = params.get('to_shop_id', False)  # Assuming 'to_shop_id' is passed in params
        to_shop_name = False
        to_shop_ph = False
        if to_shop_id:
            shop = request.env['shop.to.take'].sudo().browse(to_shop_id)
            if shop.exists():
                to_shop_name = shop.name  # Assuming 'name' field in 'shop.to.take' stores the shop name
                to_shop_ph = shop.phone  # Assuming 'phone' field in 'shop.to.take' stores the shop phone

        partner_id = request.env['res.partner'].sudo().search(
            [('x_marketing_customer', '=', True)], limit=1
        )

        # Fetch the company-specific pricelist
        pricelist = request.env['product.pricelist'].sudo().search(
            [('marketing_pricelist', '=', True)], limit=1
        )

        date_order = datetime.now()
        # Fetch sales teams where 'mobile_sale = True'
        marketing_sales_teams = request.env['crm.team'].sudo().search([('marketing_sale', '=', True)])
        # Use the first mobile sales team (or logic to determine a specific one)
        sale_team_id = marketing_sales_teams.id

        # Fetch payment terms where 'mobile_payment_term = True'
        mobile_payment_terms = request.env['account.payment.term'].sudo().search([('marketing_payment_term', '=', True)])
        payment_term_id = mobile_payment_terms.id

        # Prepare Sale Order Values
        values = {
            'partner_id': partner_id.id,
            'date_order': date_order.strftime('%Y-%m-%d %H:%M:%S'),
            'pricelist_id': pricelist.id,  # Use the fetched pricelist
            'payment_term_id': payment_term_id,
            'analytic_account_id': analytic_account.id,  # Set analytic account ID
            'warehouse_id': warehouse_id,  # Set warehouse based on the analytic account
            'sale_picking': params.get('sale_picking', "pickup"),
            'company_id': company_id,
            'commitment_date': date_order,
            'contact_ph': params.get('contact_ph', False),
            'to_shop_name': to_shop_name,  # Set the shop name
            'to_shop_ph': to_shop_ph,  # Set the shop phone
            'team_id': sale_team_id,
            'user_id': salesperson_id,
            # 'actual_start_time': params.get('actual_start_time', False),
            'payment_method_id': params.get('payment_method_id', False),
        }

        # Get available fields for sale order and sale order lines
        available_fields = request.env['sale.order'].fields_get_keys()
        available_line_fields = request.env['sale.order.line'].fields_get_keys()

        # Add additional fields from params to the sale order values
        for field in params:
            if field in available_fields:
                values[field] = params[field]

        # Fetch taxes where mobile_tax is True
        account_taxes = request.env['account.tax'].sudo().search([('marketing_tax', '=', True)])

        # Create sale order lines
        order_lines = []
        for product in params.get('products', []):
            # Fetch the product record
            product_record = request.env['product.product'].sudo().browse(product['product_id'])
            if not product_record.exists():
                return {'success': False, 'error': f'Product with ID {product["product_id"]} not found.'}

            # Fetch default UOM from product.multi_uom_line_ids
            default_uom_line = product_record.multi_uom_line_ids.filtered(lambda u: u.is_default_uom)
            if not default_uom_line:
                return {'success': False, 'error': f'Default UOM not set for product {product_record.name}.'}

            # Calculate UOM-based adjustments
            uom_ratio = default_uom_line.ratio
            # multi_uom_line = default_uom_line

            # # Use list_price from product as the price_unit
            # product_price_unit = product_record.list_price / uom_ratio

            # Calculate quantities and prices
            product_qty = product['qty'] * uom_ratio
            product_discount = product.get('discount', 0)

            # Use the provided pricelist to fetch the price
            product_price_unit = pricelist.with_context(company_id=company_id)._get_pricelist_uom_price(
                product_record, default_uom_line, product_qty)

            # Calculate total price
            total_price = product_qty * product_price_unit * (1 - product_discount / 100)

            # Prepare the order line values

            line_vals = {
                'product_id': product_record.id,
                'product_uom_qty': product_qty,  # Adjusted quantity
                'price_unit': product_price_unit,
                'discount': product_discount,  # Adjusted discount
                'multi_uom_line_id': default_uom_line.id,  # Default UOM
                'product_uom': default_uom_line.uom_id.id,  # Default UOM
                'name': product.get('description', product_record.name),  # Use provided description or product name
                'price_total': total_price,  # Total price for this line
                'tax_id': [(6, 0, account_taxes.ids)] if account_taxes else [(5, 0, 0)],
            }


            # Append to the order lines
            order_lines.append((0, 0, line_vals))

        # Add the order lines to the sale order values
        values['order_line'] = order_lines

        # Create the sale order
        order = request.env['sale.order'].sudo().create(values)

        order_name = f'{company_short_code}/SO/{short_code}/{datetime.now().strftime("%y/%m")}/{str(order.id)}'
        order.write({
            "name": order_name
        })

        # order.order_line.write({'tax_id': [(5, 0, 0)]})

        order_data = {
            "orderid": order.id,
            "customer_name": order.partner_id.name or "",
            "date_order": (order.date_order + relativedelta(hours=6, minutes=30)).strftime('%d/%m/%Y %H:%M:%S') or '',
            "total_qty": sum(line.product_uom_qty for line in order.order_line),
            "untaxed_amount": order.amount_untaxed,
            "taxes": order.amount_tax,
            "total_price": order.amount_total,
            "shop_name": order.warehouse_id.name or "",
            'order_lines': []
        }
        for line in order.order_line:
            order_data['order_lines'].append({
                'line_id': line.id,
                'product_id': line.product_id.id,
                'product_name': line.product_id.name,
                'quantity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'price_total': line.price_total,
            })

        # Return success response
        return {
            'success': True,
            'order_id': order.id,
            'name': order.name,
            'warehouse_id': warehouse_id,
            'order_data': order_data
        }


    # @http.route('/api/marketing_pricelist/products', auth='public', type='json', methods=['POST'])
    # def get_marketing_pricelist_products(self):
    #     """
    #     API to fetch products, prices, categories (from pos.category), and on-hand quantities
    #     from stock.quant for pricelists where marketing_pricelist is True,
    #     and stock.location has marketing_location=True.
    #     """
    #     # Fetch the pricelists where marketing_pricelist = True
    #     pricelists = http.request.env['product.pricelist'].sudo().search([('marketing_pricelist', '=', True)])
    #
    #     base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')  # Get the base URL of the serve
    #
    #
    #     # Prepare the products data
    #     result = []
    #     for pricelist in pricelists:
    #         for item in pricelist.item_ids:
    #             product = item.product_id
    #             if product:
    #                 # Fetch on-hand quantity from stock.quant linked to stock.location where marketing_location is True
    #                 stock_quants = http.request.env['stock.quant'].sudo().search([
    #                     ('product_id', '=', product.id),
    #                     ('location_id.marketing_location', '=', True)
    #                 ])
    #                 onhand_qty = sum(quant.quantity for quant in stock_quants)
    #
    #                 # Collect product details
    #                 product_data = {
    #
    #                     'product_id': product.id,
    #                     'product_name': product.name,
    #                     'default_code': product.default_code,
    #                     # 'product_category': product.pos_categ_id.name if product.pos_categ_id else None,
    #                     'price': item.fixed_price,
    #                     # 'list_price': product.lst_price,
    #                     'qty_available': onhand_qty,
    #                     'image': product.image_128 and product.image_128.decode('utf-8') or '',
    #                     # 'image': f"/web/image/product.product/{product.id}/image_128",
    #                     # 'image':
    #                     #     f"{base_url}/web/image/product.product/{product.id}/image_128",
    #                     'pos_categ_id': product.pos_categ_id.id if product.pos_categ_id else None,
    #                     'pos_categ_name': product.pos_categ_id.name if product.pos_categ_id else None,
    #                 }
    #                 result.append(product_data)
    #
    #     # Return the result as JSON
    #     return {
    #         'status': 'success',
    #         'pricelist_name': pricelist.name,
    #         'product data': result,
    #     }


    @http.route('/api/marketing_pricelist/products/old', auth='public', type='json', methods=['POST'])
    def get_marketing_pricelist_products_old(self):
        """
        API to fetch products, prices, categories (from pos.category), and on-hand quantities
        from stock.quant for pricelists where marketing_pricelist is True,
        and stock.location has marketing_location=True.
        """

        # Fetch the pricelists where marketing_pricelist = True
        pricelists = http.request.env['product.pricelist'].sudo().search([('marketing_pricelist', '=', True)])

        # base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')  # Get the base URL of the serve

        # Prepare the products data
        result = []
        for pricelist in pricelists:
            for item in pricelist.item_ids:
                product = item.product_id


                if product:
                    # Fetch on-hand quantity from stock.quant linked to stock.location where marketing_location is True
                    stock_quants = http.request.env['stock.quant'].sudo().search([
                        ('product_id', '=', product.id),
                        ('location_id.marketing_location', '=', True)
                    ])
                    onhand_qty = sum(quant.quantity for quant in stock_quants)

                    # image_base64 = ''
                    # if product.image_1920:
                    #     original_image = base64.b64decode(product.image_1920)
                    #     image = Image.open(BytesIO(original_image))
                    #     image.thumbnail(size)
                    #     buffer = BytesIO()
                    #     image.save(buffer, format=image.format)
                    #     return base64.b64encode(buffer.getvalue()).decode('utf-8')

                    # Collect product details
                    product_data = {

                        'product_id': product.id,
                        'product_name': product.name,
                        'default_code': product.default_code,
                        # 'product_category': product.pos_categ_id.name if product.pos_categ_id else None,
                        'price': item.fixed_price,
                        # 'list_price': product.lst_price,
                        'qty_available': onhand_qty,
                        # 'image': image_base64,
                        'image': product.image_128 and product.image_128.decode('utf-8') or '',
                        # 'image_url': f"/web/image/product.product/{product.id}/image_128",
                        # 'image':
                        # f"{base_url}/web/image/product.product/{product.id}/image_128",
                        # if product.image_128
                        # else f"{base_url}/web/static/src/img/placeholder.png",  # Default placeholder image

                        'pos_categ_id': product.pos_categ_id.id if product.pos_categ_id else None,
                        'pos_categ_name': product.pos_categ_id.name if product.pos_categ_id else None,
                    }
                    result.append(product_data)

        # Return the result as JSON
        return {
            'status': 'success',
            'pricelist_name': pricelist.name,
            'product_data': result,
        }

    @http.route('/api/marketing_pricelist/products', auth='public', type='json', methods=['POST'])
    def get_marketing_pricelist_products(self):
        """
        API to fetch products, prices, categories (from pos.category), and on-hand quantities
        from stock.quant for pricelists where marketing_pricelist is True,
        and stock.location has marketing_location=True.
        """

        def resize_image(base64_str, size=(512, 512)):
            """
            Resizes the input Base64 image to the specified size and returns the resized image in Base64.
            """
            if not base64_str:
                return ''
            try:
                image_data = base64.b64decode(base64_str)
                image = Image.open(BytesIO(image_data))
                image.thumbnail(size)  # Resize the image
                buffer = BytesIO()
                image_format = image.format if image.format else "PNG"
                image.save(buffer, format=image_format)
                return base64.b64encode(buffer.getvalue()).decode('utf-8')
            except Exception as e:
                return ''  # Return empty string in case of error

        # Fetch the pricelists where marketing_pricelist = True
        pricelists = request.env['product.pricelist'].sudo().search([('marketing_pricelist', '=', True)])

        # Prepare the products data
        result = []
        for pricelist in pricelists:
            for item in pricelist.item_ids:
                product = item.product_id
                if product:
                    # Fetch on-hand quantity from stock.quant linked to stock.location where marketing_location is True
                    stock_quants = request.env['stock.quant'].sudo().search([
                        ('product_id', '=', product.id),
                        ('location_id.marketing_location', '=', True)
                    ])
                    onhand_qty = sum(quant.quantity for quant in stock_quants)

                    # Resize the product image
                    image_base64 = resize_image(product.image_1920, size=(512, 512)) if product.image_1920 else ''

                    # Collect product details
                    product_data = {
                        'product_id': product.id,
                        'product_name': product.name,
                        'default_code': product.default_code,
                        'price': item.fixed_price,
                        'qty_available': onhand_qty,
                        'image': image_base64,
                        'pos_categ_id': product.pos_categ_id.id if product.pos_categ_id else None,
                        'pos_categ_name': product.pos_categ_id.name if product.pos_categ_id else None,
                    }
                    result.append(product_data)

        # Return the result as JSON
        return {
            'status': 'success',
            'pricelist_name': pricelists[0].name if pricelists else None,
            'product_data': result,
        }

    @http.route('/api/get/employee', type='json', auth='user', methods=['POST'], csrf=False)
    def get_employee_info(self, **kwargs):
        """
        Fetch the employee name associated with a given user_id.
        """
        user_id = request.jsonrequest.get('user_id')

        # Ensure the user_id exists and fetch the user and employee details
        if user_id:
            user = request.env['res.users'].sudo().browse(user_id)
            if user.exists():
                employee_name = user.employee_id.name if user.employee_id else None
                return {
                    'status': 'success',
                    'user_id': user_id,
                    'employee_name': employee_name
                }
            else:
                return {
                    'status': 'error',
                    'message': 'User not found'
                }