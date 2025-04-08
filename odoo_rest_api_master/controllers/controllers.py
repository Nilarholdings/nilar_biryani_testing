# -*- coding: utf-8 -*-
import json
import math
import logging
import requests
import re

from odoo import http, _, exceptions
from odoo.http import request
from datetime import datetime



from odoo.http import request




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
    @http.route('/api/auth/login', type='json', auth='none', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        # Your code here
        return {'status': 'success'}
    # for authenticate
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

    # # for all product
    # @http.route(
    #     '/api/products',
    #     type='json', auth='user', methods=["POST"], csrf=False
    # )
    # def get_products(self, **post):
    #     domain = []
    #     args = []
    #     kwargs = {}
    #     # Extract 'args' and 'kwargs' from the JSON payload, if provided
    #     if "args" in post:
    #         args = post["args"]
    #     if "kwargs" in post:
    #         kwargs = post["kwargs"]
    #     # Perform search_read on the 'product.template' model
    #     products = request.env['product.template'].search_read(
    #         domain,
    #         fields=['name', 'list_price', 'default_code', 'qty_available'],
    #         *args, **kwargs
    #     )
    #     # Return the products data in JSON format
    #     return products


    # //saleable product-category

    # category
    @http.route(
        '/api/category',
        type='json', auth='user', methods=["POST"], csrf=False)
    def call_product_category_function(self):
        domain = []
        categories = request.env['product.category'].search([('x_selling_category', '=', True)])

        result = [{
            'id': category.id,
            'name': category.name,

        } for category in categories]
        return result


    # saleable product by category
    @http.route('/api/category/products', type='json', auth='public', methods=['POST'])
    def get_saleable_products_by_category(self, **kwargs):
        # Retrieve category_id from the request's JSON payload
        param = request.jsonrequest
        print(param)
        category_id = param.get('category_id')

        # Ensure category_id is provided
        if not category_id:
            return {"error": "category_id is required"}

        # Fetch products with the given category_id
        products = request.env['product.template'].search([('categ_id', '=', category_id), ('categ_id.x_selling_category', '=', True)])

        # Format product data for the response
        product_data = [{
            'id': product.id,
            'name': product.name,
            'default_code': product.default_code,
            'list_price': product.list_price,
            'categ_id': product.categ_id.id,
            'qty_available': product.qty_available,
            'image': product.image_1920 and product.image_1920.decode('utf-8') or '',
        } for product in products]

        # return {
        #     "category_id": category_id,
        #     "products": product_data
        # }

        # Return the response
        return product_data

    # saleable product
    @http.route('/api/products', type='json', auth='public', methods=['POST'])
    def get_saleable_products(self, **kwargs):

        # Fetch products with the given category_id
        products = request.env['product.template'].search([('categ_id.x_selling_category', '=', True)])

        # Format product data for the response
        product_data = [{
            'id': product.id,
            'name': product.name,
            'default_code': product.default_code,
            'list_price': product.list_price,
            'categ_id': product.categ_id.id,
            'qty_available': product.qty_available,
            'image': product.image_1920 and product.image_1920.decode('utf-8') or '',
        } for product in products]
        # Return the response
        return product_data

    # saleable product with pagination
    @http.route('/api/category/products/pagination', type='json', auth='public', methods=['POST'])
    def get_saleable_products_pagination(self, **kwargs):
        param = request.jsonrequest # change json format
        limit = param.get('limit', 10)  # Number of records per page
        offset = param.get('offset', 0) # Starting record for each page

        products = request.env['product.template'].search([('categ_id.x_selling_category', '=', True)],limit=limit, offset=offset)
        # Format product data for the response
        product_data = [{
            'id': product.id,
            'name': product.name,
            'default_code': product.default_code,
            'list_price': product.list_price,
            'categ_id': product.categ_id.id,
            'qty_available': product.qty_available,
            'image': product.image_1920 and product.image_1920.decode('utf-8') or '',
        } for product in products]
        # Return the response
        return product_data

    # pos location
    @http.route('/api/location', type='json', auth='user', methods=['POST'])
    def get_all_pos_details(self):
        """
        API endpoint to retrieve all POS configurations with their details.
        """
        # Search for all pos.location records without any limit
        pos_locations = request.env['pos.location'].sudo().search([])

        # Check if any POS configurations are found
        if not pos_locations:
            return {"error": "No POS Location records found"}

        # Prepare response data for each POS location
        response_data = []
        for pos_config in pos_locations:
            response_data.append({
                'pos_config_id': pos_config.id,
                'pos_name': pos_config.name,
                'location_id': pos_config.location_id.id,
                'location_name': pos_config.location_id.display_name,
                'analytic_account_id': pos_config.analytic_account_id.id if pos_config.analytic_account_id else None,
                'analytic_account_name': pos_config.analytic_account_id.name if pos_config.analytic_account_id else None,
            })

        # Return the response
        return response_data

    @http.route('/api/location/product', type='json', auth='user', methods=['POST'])
    def get_pos_details_by_location(self):
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
            'image': quant.product_id.image_1920 and quant.product_id.image_1920.decode('utf-8') or ''
        } for quant in stock_quants]

        # Prepare the response
        response_data = {
            'location_id': location.id,
            'location_name': location.display_name,
            'products': products,
        }

        return response_data

    # mobile customer
    @http.route('/api/mobile_customers', type='json', auth='user', methods=["POST"], csrf=False)
    def get_mobile_customers(self, **post):
        """
        API to fetch customers with optional filters using 'args' and 'kwargs'.
        """
        domain = [('x_is_a_mobile', '=', True)]  # Base filter to only get customers
        args = []
        kwargs = {}

        # Extract 'args' and 'kwargs' from the request payload, if provided
        if "args" in post:
            args = post["args"]
        if "kwargs" in post:
            kwargs = post["kwargs"]

        # Perform search_read on the 'res.partner' model
        customers = request.env['res.partner'].search_read(
            domain,
            fields=[ 'name', 'email', 'phone', 'street', 'city', 'country_id'],
            *args, **kwargs
        )

        # Format the country data
        for customer in customers:
            if customer.get('country_id'):
                customer['country_name'] = customer['country_id'][1]  # Add the country name
                customer['country_id'] = customer['country_id'][0]  # Keep only the ID for 'country_id'

        return customers

    # all customer
    @http.route('/customers', type='json', auth='user', methods=["POST"], csrf=False)
    def get_customers(self, **post):
        """
        API to fetch customers with optional filters using 'args' and 'kwargs'.
        """
        domain = []  # Base filter to only get customers
        args = []
        kwargs = {}

        # Extract 'args' and 'kwargs' from the request payload, if provided
        if "args" in post:
            args = post["args"]
        if "kwargs" in post:
            kwargs = post["kwargs"]

        # Perform search_read on the 'res.partner' model
        customers = request.env['res.partner'].search_read(
            domain,
            fields=['id', 'name', 'email', 'phone', 'street', 'city', 'country_id'],
            *args, **kwargs
        )

        # Format the country data
        for customer in customers:
            if customer.get('country_id'):
                customer['country_name'] = customer['country_id'][1]  # Add the country name
                customer['country_id'] = customer['country_id'][0]  # Keep only the ID for 'country_id'

        return customers

    # from mobile , mobile customer
    @http.route('/api/customer', type='json', auth='user', methods=['POST'])
    def get_api_customers(self):
        """
        Retrieves customer details. Supports filtering by customer ID, name, email, or phone.
        """
        # Retrieve parameters from the request
        params = request.jsonrequest if request.jsonrequest else request.params

        # Prepare the domain for filtering customers
        domain = []  # Ensure we only fetch customers

        # Filter by specific fields if provided
        if params.get('customer_id'):
            domain.append(('id', '=', params.get('customer_id')))
        if params.get('name'):
            domain.append(('name', 'ilike', params.get('name')))
        if params.get('email'):
            domain.append(('email', 'ilike', params.get('email')))
        # Validate and constrain the phone number format if provided
        if params.get('phone'):
            phone = params.get('phone')
            # Regular expression for validating phone numbers (e.g., 0123456789 or +1234567890)
            # phone_regex = re.compile(r'^\+?[0-9]{10,15}$')  # Adjust the pattern as needed
            # if not phone_regex.match(phone):
            #     return {'success': False, 'error': 'Invalid phone number '}
            domain.append(('phone', '=', phone))  # Filter by phone number

        if params.get('x_is_a_mobile'):
            domain.append(('x_is_a_mobile', 'ilike', bool(params.get('x_is_a_mobile'))))

        # Search for customers based on the domain
        customers = request.env['res.partner'].sudo().search(domain)

        # Check if any customers are found
        if not customers:
            return {'success': False, 'error': 'No Customer found'}

        # Prepare the response data
        response_data = []
        for customer in customers:
            response_data.append({
                'customer_id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'street': customer.street,
                'city': customer.city,
                'mobile': customer.x_is_a_mobile,
                'state': customer.state_id.name,
                'country': customer.country_id.name if customer.country_id else None,
                'x_is_a_mobile': True,  # Set x_is_a_mobile to True
                'customer': True,
                'x_mobile_latitude': customer.x_mobile_latitude,
                'x_mobile_longitude': customer.x_mobile_longitude,
            })


        return {
            'success': True,

            'customer': response_data
        }

    # customer create from mobile
    @http.route('/customer/add', type='json', auth='user', methods=['POST'], csrf=False)
    def add_customer(self, **kwargs):
        try:
            # Parse request data
            customer_data = request.jsonrequest

            # Validate required fields
            if not customer_data.get('name'):
                return {'success': False, 'error': 'The field "name" is required to create a customer.'}

            if not customer_data.get('phone'):
                return {'success': False, 'error': 'The field "phone" is required to create a customer.'}

            # Prepare values for creating a customer
            vals = {
                'name': customer_data.get('name'),  # Required field
                'email': customer_data.get('email', False),
                'phone': customer_data.get('phone', False),
                'mobile': customer_data.get('mobile', False),
                'x_is_a_mobile': True,  # Set x_is_a_mobile to True
                'customer': True,
                'street': customer_data.get('street', False),
                'street2': customer_data.get('street2', False),
                'x_city_id': customer_data.get('x_city_id', False),
                'city': customer_data.get('city', False),
                'state_id': customer_data.get('state_id', False),
                'country_id': customer_data.get('country_id', False),
                'x_mobile_latitude': customer_data.get('x_mobile_latitude', False),
                'x_mobile_longitude': customer_data.get('x_mobile_longitude', False),


                # 'zip': customer_data.get('zip', False),
                # 'customer_rank': 1,  # Mark this contact as a customer
            }

            # Create the customer record in res.partner
            customer = request.env['res.partner'].sudo().create(vals)

            # Update specific fields after creation
            customer.sudo().write({
                # 'name': f"Customer-{customer.id}",  # Update the name with a custom value
                'display_name': customer.name,  # Update the name with a custom value

            })

            return {
                'success': True,
                'message': 'Customer created and updated successfully.',
                'customer_id': customer.id,
                'customer_name': customer.name,
            }

        except Exception as e:
            # Rollback in case of an error
            request.env.cr.rollback()
            return {'success': False, 'error': str(e)}

    # for all country
    @http.route('/api/country',type='json', auth='user', methods=["POST"], csrf=False)
    def get_countries(self, **post):
        domain = []
        # Perform search_read on the 'res.country' model
        country = request.env['res.country'].search_read(domain,
            fields=['id', 'name', 'code', 'default_country'],
        )
        # Return the countries data in JSON format
        return country

    # for all state
    @http.route('/api/states',type='json', auth='user', methods=["POST"], csrf=False)
    def get_states(self, **post):
        domain = []
        # Perform search_read on the 'res.country.state' model
        states = request.env['res.country.state'].search_read(domain,
            fields=['id', 'name', 'code', 'country_id'],
        )
        # Return the states data in JSON format
        return states

    # choose country_id get state
    @http.route('/api/country/state', type='json', auth='user', methods=['POST'])
    def get_state_by_country(self):
        """
        Retrieve state for a specific country, including
        """
        # Retrieve country_id from the JSON payload
        country_id = request.jsonrequest.get('country_id')
        if not country_id:
            return {"error": "Country ID is required"}

        # Check if the location exists
        country = request.env['res.country'].sudo().browse(country_id)
        if not country.exists():
            return {"error": f"Country with ID {country_id} does not exist"}

        # Fetch  the country
        states = request.env['res.country.state'].sudo().search([
            ('country_id', '=', country.id),

        ])

        state_data = [{
            'id': state.id,
            'name': state.name,
            'code': state.code,
        } for state in states]

        # Prepare the response
        response_data = {
            'success': True,
            'country_id': country.id,
            'country_name': country.name,
            'states': state_data,
        }

        return response_data

    @http.route('/api/state/cities', type='json', auth='user', methods=['POST'])
    def get_cities_by_state(self):
        """
        Retrieve cities for a specific state, including state and country information.
        """
        # Retrieve state_id from the JSON payload
        state_id = request.jsonrequest.get('state_id')
        if not state_id:
            return {"error": "State ID is required"}

        # Check if the state exists
        state = request.env['res.country.state'].sudo().browse(state_id)
        if not state.exists():
            return {"error": f"State with ID {state_id} does not exist"}

        # Fetch cities for the given state
        cities = request.env['res.city'].sudo().search([('state_id', '=', state.id)])

        # Prepare the city data
        city_data = [{
            'id': city.id,
            'name': city.name,
            'code': city.code,  # Assuming the 'code' field exists
            'state_id': city.state_id.id if city.state_id else None,  # Retrieve the state ID
            'country_id': city.country_id.id if city.country_id else None,  # Retrieve the country ID
        } for city in cities]

        # Prepare the response
        response_data = {
            'success': True,
            'state_id': state.id,
            'state_name': state.name,
            'country_id': state.country_id.id,
            'country_name': state.country_id.name,
            'cities': city_data,
        }

        return response_data
    # shop
    @http.route('/api/shop', type='json', auth='user', methods=["POST"], csrf=False)
    def get_shop(self, **post):
        domain = []
        # Perform search_read on the 'shop.to.take' model
        shops = request.env['shop.to.take'].search_read(domain,
                                                        fields=['id', 'name', 'phone'],
                                                        )
        # Return the shops data in JSON format
        return shops

    # for all multi_uom
    @http.route('/api/multi_uom_line', type='json', auth='user', methods=["POST"], csrf=False)
    def get_multi_uom(self, **post):
        domain = []
        # Perform search_read on the 'multi.uom.line' model
        multi_uom = request.env['multi.uom.line'].search_read(domain,
                                                              fields=['uom_id', 'price', 'ratio', 'product_tmpl_id',
                                                                      'is_default_uom', 'uom_code'],
                                                       )
        # Return the multi_uom_line data in JSON format
        return multi_uom

    # taxes
    @http.route('/api/taxes', type='json', auth='user', methods=["POST"], csrf=False)
    def get_taxes(self, **post):
        """
        Retrieve tax details from the account.tax model.
        """
        domain = []
        # Apply filters from post data if provided
        if 'type_tax_use' in post:
            domain.append(('type_tax_use', '=', post['type_tax_use']))
        if 'amount' in post:
            domain.append(('amount', '=', post['amount']))

        # Search and read tax data
        taxes = request.env['account.tax'].sudo().search_read(
            domain,
            fields=['id', 'name', 'amount', 'type_tax_use', 'amount_type', 'active','description','tax_group_id','analytic','price_include','include_base_amount','is_base_affected'])

        return taxes

    # cities
    @http.route('/api/cities', type='json', auth='public', methods=['POST'], csrf=False)
    def get_cities(self):
        # Retrieve all cities (or you can filter this based on specific criteria)
        cities = request.env['res.city'].sudo().search([])  # Replace with any filtering if needed

        # Prepare the data to be returned
        city_data = []
        for city in cities:
            city_data.append({
                'id': city.id,
                'name': city.name,
                'code': city.code,  # Assuming there's a code field
                'state_id': city.state_id.id if city.state_id else None,  # Retrieve state_id
                'country_id': city.country_id.id if city.country_id else None,  # Retrieve country_id
            })

        return {'cities': city_data}

    # delivery address
    @http.route('/create_delivery_address', type='json', auth='user', methods=['POST'], csrf=False)
    def create_delivery_address(self):
        # Get the JSON data from the POST request
        data = request.jsonrequest
        customer_id = data.get('customer_id')

        if not customer_id:
            return {'error': 'customer_id is required'}

        # Find the customer (res.partner) record
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if not customer.exists():
            return {'error': 'Customer not found'}

        # Create a new delivery address record (a child of the customer)
        delivery_address = request.env['res.partner'].sudo().create({
            'name': data.get('address_name', 'Default Address Name'),
            'type': 'delivery',
            'parent_id': customer.id,
            'street': data.get('street', False),
            'street2': data.get('street2', False),
            'city': data.get('city', False),
            'x_city_id': data.get('x_city_id', False),
            'state_id': data.get('state_id', False),
            'zip': data.get('zip', False),
            'email': data.get('email', False),
            # 'phone': data.get('phone', False),
            # 'mobile': data.get('mobile', False),
            'x_mobile_latitude': data.get('x_mobile_latitude', False),
            'x_mobile_longitude': data.get('x_mobile_longitude', False),
            'country_id': data.get('country_id', False),  # You can pass country ID here
        })

        # The delivery address is automatically added to the customer's child_ids
        # because we set the parent_id to the customer.
        return {'Remark': 'Delivery address created successfully', 'success': True, 'address_id': delivery_address.id}

    # create delivery address
    @http.route('/get_customer_delivery_details', type='json', auth='public', methods=['POST'], csrf=False)
    def get_customer_delivery_details(self):
        # Get the JSON data from the request
        data = request.jsonrequest
        customer_id = data.get('customer_id')

        if not customer_id:
            return {'error': 'customer_id is required'}

        # Find the parent customer
        customer = request.env['res.partner'].sudo().browse(customer_id)
        if not customer.exists():
            return {'error': 'Customer not found'}

        # Prepare the response with parent and delivery address details
        response = {
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
                'phone': customer.phone,
                'street': customer.street,
                'street2': customer.street2,
                'x_city_id': customer.x_city_id.name,
                'state_id': customer.state_id.name if customer.state_id.name else None,
                'city': customer.city,
                'zip': customer.zip,
                'x_mobile_latitude': customer.x_mobile_latitude,
                'x_mobile_longitude':customer.x_mobile_longitude,
                'country_id': customer.country_id.name if customer.country_id.name else None,
            },
            'delivery_addresses': [
                {
                    'id': child.id,
                    'name': child.name,
                    'type': child.type,
                    'street': child.street,
                    'street2': child.street2,
                    'x_city_id': child.x_city_id.name,
                    'city': child.city,
                    'zip': child.zip,
                    'x_mobile_latitude': child.x_mobile_latitude,
                    'x_mobile_longitude': child.x_mobile_longitude,
                    'state_id': child.state_id.name if child.state_id.name else None,
                    'country_id': child.country_id.name if child.country_id.name else None,
                }
                for child in customer.child_ids if child.type == 'delivery'
            ],
        }

        return {'success': True, 'data': response}

    # create sale order
    @http.route('/api/create/sale-orders', type='json', auth='none', methods=['POST'], csrf=False)
    def create_pre_sale_order(self, **kwargs):
        params = request.jsonrequest
        uid = request.session.uid
        if not uid:
            return {'success': False, 'error': 'Invalid cookie.'}

        company_id = request.env['res.users'].sudo().browse(uid).company_id.id

        # Fetch the company's short code
        company = request.env['res.company'].sudo().browse(company_id)
        company_short_code = company.short_code or "N/A"

        # Get the analytic account id from params
        analytic_account_id = params.get('analytic_account_id', False)
        warehouse_id = False
        short_code = None

        # branch = self.env['res.company'].browse('company_id')
        # branch_code = branch.short_code

        if analytic_account_id:
            # Get the analytic account and associated warehouse
            analytic_account = request.env['account.analytic.account'].sudo().browse(analytic_account_id)
            if analytic_account.exists():
                # If an analytic account exists, fetch the related warehouse using location_id
                warehouse_id = analytic_account.location_id and analytic_account.location_id.warehouse_id.id
                short_code= analytic_account.short_code  # Access the shot_code field

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

        # Fetch the company-specific pricelist
        pricelist = request.env['product.pricelist'].sudo().search(
            [('mobile_pricelist', '=', True)], limit=1
        )

        # Fetch sales teams where 'mobile_sale = True'
        mobile_sales_teams = request.env['crm.team'].sudo().search([('mobile_sale', '=', True)])
        # Use the first mobile sales team (or logic to determine a specific one)
        sale_team_id = mobile_sales_teams.id

        # Fetch payment terms where 'mobile_payment_term = True'
        mobile_payment_terms = request.env['account.payment.term'].sudo().search([('mobile_payment_term', '=', True)])
        payment_term_id = mobile_payment_terms.id

        # Prepare Sale Order Values
        values = {
            'partner_id': params.get('partner_id', False),
            'partner_invoice_id': params.get('partner_invoice_id', False),
            'partner_shipping_id': params.get('partner_shipping_id', False),
            'date_order': params.get('date_order', False),
            'pricelist_id': pricelist.id,  # Use the fetched pricelist
            'currency_id': params.get('currency_id', False),
            'payment_term_id': payment_term_id,
            'analytic_account_id': analytic_account_id,  # Set analytic account ID
            'warehouse_id': warehouse_id,  # Set warehouse based on the analytic account
            'user_id': params.get('user_id', False),
            'sale_picking': params.get('sale_picking', False),
            'company_id': company_id,
            'commitment_date': params.get('commitment_date', False),
            'contact_ph': params.get('contact_ph', False),
            'to_shop_name': to_shop_name,  # Set the shop name
            'to_shop_ph': to_shop_ph,  # Set the shop phone
            'team_id': sale_team_id,
            'actual_start_time': params.get('actual_start_time', False),
        }

        # Get available fields for sale order and sale order lines
        available_fields = request.env['sale.order'].fields_get_keys()
        available_line_fields = request.env['sale.order.line'].fields_get_keys()

        # Add additional fields from params to the sale order values
        for field in params:
            if field in available_fields:
                values[field] = params[field]

        # Fetch taxes where mobile_tax is True
        account_taxes = request.env['account.tax'].sudo().search([('mobile_tax', '=', True)])

        # Create sale order lines
        order_lines = []
        for product in params.get('products', []):
            # Fetch the product record
            product_record = request.env['product.product'].sudo().search(
                [('product_tmpl_id', '=', product['product_id'])])
            if not product_record.exists():
                return {'success': False, 'error': f'Product with ID {product["product_id"]} not found.'}



            # Fetch default UOM from product.multi_uom_line_ids
            default_uom_line = product_record.multi_uom_line_ids.filtered(lambda u: u.is_default_uom)
            if not default_uom_line:
                return {'success': False, 'error': f'Default UOM not set for product {product_record.name}.'}

            # Calculate UOM-based adjustments
            uom_ratio = default_uom_line.ratio
            # multi_uom_line = default_uom_line

            # Use list_price from product as the price_unit
            product_price_unit = product_record.list_price / uom_ratio

            # Calculate quantities and prices
            product_qty = product['qty'] * uom_ratio
            product_discount = product.get('discount', 0)

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
                'tax_id': [(6, 0, account_taxes.ids)],
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


        # Return success response
        return {
            'success': True,
            'order_id': order.id,
            'name': order.name,
            'warehouse_id': warehouse_id,

        }

    # sale order history
    # @http.route('/api/sale_order_history', type='json', auth='user')
    # def get_sale_orders_by_customer(self, customer_id=None):
    #     data = request.jsonrequest
    #     customer_id = data.get('customer_id')
    #     if not customer_id:
    #         return {"error": "Customer ID is required"}
    #
    #     # Fetch the customer
    #     customer = request.env['res.partner'].sudo().search([('id', '=', customer_id),('x_is_a_mobile', '=', True)], limit=1)
    #     if not customer:
    #         return {"error": "Customer not found"}
    #
    #     # Fetch sale orders for the customer
    #     sale_orders = request.env['sale.order'].sudo().search([('partner_id', '=', customer.id)])
    #     if not sale_orders:
    #         return {"message": "No sale orders found for this customer"}
    #
    #     # Prepare the response data
    #     orders_data = []
    #     for sale_order in sale_orders:
    #         shipping_partner = sale_order.partner_shipping_id or sale_order.partner_id
    #
    #         # Get detailed address components
    #         address = {
    #             "street": shipping_partner.street or "",
    #             "street2": shipping_partner.street2 or "",
    #             "city": shipping_partner.city or "",
    #             "state": shipping_partner.state_id.name if shipping_partner.state_id else "",
    #             "country": shipping_partner.country_id.name if shipping_partner.country_id else "",
    #         }
    #
    #         order_data = {
    #             "orderid": sale_order.id,
    #             "customer_name": sale_order.partner_id.name or "",
    #             "date_time": sale_order.date_order or "",
    #             "total_qty": sum(line.product_uom_qty for line in sale_order.order_line),
    #             "total_price": sale_order.amount_total,
    #             "shop_name": sale_order.warehouse_id.name or "",
    #             "address": address,
    #             "proudct": [
    #                 {
    #                     "name": line.product_id.name,
    #                     "qty": line.product_uom_qty,
    #                     "price": line.price_subtotal
    #                 }
    #                 for line in sale_order.order_line
    #             ]
    #         }
    #         orders_data.append(order_data)
    #
    #     return orders_data

    @http.route('/api/sale_order_history', type='json', auth='user')
    def get_sale_orders_by_customer(self, customer_id=None):
        data = request.jsonrequest
        customer_id = data.get('customer_id')
        if not customer_id:
            return {'error': 'Customer ID is required'}

        # Fetch sales teams where 'mobile_sale = True'
        mobile_sales_teams = request.env['crm.team'].sudo().search([('mobile_sale', '=', True)])
        if not mobile_sales_teams:
            return {'error': 'No mobile sales teams found'}

        # Use the first mobile sales team
        sale_team_id = mobile_sales_teams[0].id

        # Fetch sale orders for the given customer
        sale_orders = request.env['sale.order'].search([
            ('partner_id', '=', int(customer_id)),
            ('team_id', '=', sale_team_id),  # Filter by sales team

        ])

        if not sale_orders:
            return {'error': 'No sale orders found for the given customer'}

        result = []
        for order in sale_orders:
            shipping_partner = order.partner_shipping_id or order.partner_id

            delivery_address = {
                'id': shipping_partner.id,
                'name': shipping_partner.name,
                "street": shipping_partner.street or "",
                "street2": shipping_partner.street2 or "",
                'x_city_id': shipping_partner.x_city_id.name,
                "city": shipping_partner.city or "",
                "state": shipping_partner.state_id.name if shipping_partner.state_id else "",
                "country": shipping_partner.country_id.name if shipping_partner.country_id else "",
                'x_mobile_latitude': shipping_partner.x_mobile_latitude,
                'x_mobile_longitude': shipping_partner.x_mobile_longitude,
            }

            order_data = {
                "orderid": order.id,
                "customer_name": order.partner_id.name or "",
                "date_time": order.date_order or "",
                "total_qty": sum(line.product_uom_qty for line in order.order_line),
                "untaxed_amount": order.amount_untaxed,
                "taxes": order.amount_tax,  # Detailed tax breakdown
                "total_price": order.amount_total,
                "shop_name": order.warehouse_id.name or "",
                'state': order.state,
                "delivery_address": delivery_address,
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