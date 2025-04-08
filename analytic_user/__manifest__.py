# -*- coding: utf-8 -*-
{
    'name': 'User Form Access',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 1001,
    'summary': 'Analytic account in all journals',
    'author': 'Nilar Binary',
    'depends': [
        'base',
        'account',
        'point_of_sale',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_location_form_view.xml',
        'views/res_user_views.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
