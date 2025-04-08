# -*- coding: utf-8 -*-
{
    'name': 'POS Product Filter By Location',
    'version': '1.0',
    'category': 'Point of Sale',
    'sequence': 1000,
    'author': 'Nilar ',
    'depends': ['point_of_sale'],
    'data': [
        'views/assets.xml',
        'views/pos_views.xml',
    ],
    'qweb': [
        'static/src/xml/ProductList.xml',

    ],
    'application': True,
    'license': 'LGPL-3',
    'assets': {
        'point_of_sale.assets': [
            'pos_product_filter_by_location/static/src/js/Screens/PaymentScreen.js',
            'pos_product_filter_by_location/static/src/js/Screens/ProductScreen.js',
            'pos_product_filter_by_location/static/src/js/model.js',
        ],
        'web.assets_qweb': [
            'pos_product_filter_by_location/static/src/xml/*',
        ],
    },
}
