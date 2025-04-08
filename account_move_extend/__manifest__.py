# -*- coding: utf-8 -*-
{
    'name': "Account Extend",

    'summary': """To Show Contact Name in Invoice Form""",

    'description': """
        1.Account Move Extend  
    """,

    'author': "Asia Matrix",
    'website': "www.asiamatrixsoftware.com",

    'category': 'account',
    'version': '1.8',
    'license': "LGPL-3",

    'depends': [
        'account',
        'sale',
        'account_asset'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_move_line_views.xml',
    ],

}
