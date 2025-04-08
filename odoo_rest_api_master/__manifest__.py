# -*- coding: utf-8 -*-
{
    'name': "Biryani Mobile Connector(Api)",

    'summary': """
        Biryani Mobile Connector""",

    'description': """
        Biryani Mobile Connector
    """,

    'author': "Nilar",


    'category': 'Api',
    'version': '2.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'contacts',
        'product_extend', 'web',
        'stock','sale', 'analytic_user'],

    'data': [
        'security/ir.model.access.csv',
        'views/res_city_views.xml',
        'views/api_data_views.xml',

    ],

    "application": True,
    "installable": True,
    "auto_install": False,

    'external_dependencies': {
        'python': ['pypeg2']
    }
}