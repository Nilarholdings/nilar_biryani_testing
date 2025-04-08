# -*- coding: utf-8 -*-
{
    'name': "User Access Right",

    'summary': """Access Right Module""",

    'description': """
        This Module Add user access right.
    """,

    'author': "Asia Matrix Software Solution",

    'website': "http://www.asiamatrixsoftware.com",

    'category': 'Security',

    'version': '1.2',

    'license': 'LGPL-3',

    'depends': [
        'stock_account',
        'stock_requestion',
        'point_of_sale',
        'sale_requisition',
        'sale_order_extend',
        'nilar_purchase_requisition',
        'purchase_extend',
        'mrp',
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',
        'security/point_of_sale_security.xml',
        'security/product_cost_access.xml',
        'security/stock_requisition_access.xml',
        'security/submission_access.xml',
        'security/purchase_requisition_access.xml',
        'security/purchase_order_access.xml',
        'security/sale_requisition_access.xml',
        'security/sale_order_access.xml',
        'security/mrp_access_views.xml',
        'views/sale_access_views.xml',
        'views/sale_requisition_views.xml',
        'views/stock_requisition_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_requisition_views.xml',
        'views/submission_views.xml',
        'views/stock_views.xml',
        'views/point_of_sale_views.xml',
        'views/vendor_pricelist_views.xml',
        'views/product_views.xml',
        'views/product_template_views.xml',

    ],

    'images': ['static/description/icon.png'],
}
