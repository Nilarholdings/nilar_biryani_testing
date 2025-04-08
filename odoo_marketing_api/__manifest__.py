# -*- coding: utf-8 -*-
{
    'name': "Biryani Marketing (Api)",

    'summary': """
        Biryani Mobile Marketing Connector""",

    'description': """
        Biryani Mobile Connector
    """,

    'author': "Nilar",


    'category': 'Api',
    'version': '3.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'point_of_sale', 'contacts',
        'product_extend', 'web',
        'stock','sale', 'analytic_user','account'],

    'data': [


        'views/marketing_api_data_views.xml',

    ],

    "application": True,
    "installable": True,
    "auto_install": False,

    'external_dependencies': {
        'python': ['pypeg2']
    }
}