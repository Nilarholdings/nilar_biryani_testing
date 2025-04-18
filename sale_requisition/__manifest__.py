# -*- coding: utf-8 -*-
{
    'name': "Sale Requisition",

    'summary': """For Sale Requisition """,

    'description': """
        For Sale Requisition 
    """,

    'author': "Asiamatrix",

    'website': "http://www.asiamatrixsoftware.com",

    'category': 'sale',

    'version': '7.9',

    'license': "LGPL-3",

    'depends': [
        'sale',
        'mail',
        'stock',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence_code.xml',
        'views/sale_order_view.xml',
        'views/whole_sale_view.xml',
        'views/stock_location_views.xml',
        'views/res_users_views.xml',
        'views/stock_picking_view.xml',
    ],

    'installable': True,
    'application': False,
}
