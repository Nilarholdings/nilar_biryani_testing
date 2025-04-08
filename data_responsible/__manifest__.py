# -*- coding: utf-8 -*-
{
    'name': 'Data Responsible',
    'version': '0.5',
    'category': 'Extra',
    'sequence': 999,
    'summary': 'Responsilbe Person/Group for master data',
    'author': 'Nilar Odoo',
    'depends': [
        'point_of_sale',
        'product_extend',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/data_responsible_views.xml',
        'views/master_data_views.xml'
    ],
    'application': False,
    'license': 'LGPL-3',
    'installable' : True
}
