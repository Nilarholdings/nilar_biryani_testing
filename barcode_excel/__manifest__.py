# -*- coding: utf-8 -*-

{
    'name': 'Barcode Excel for Product',
    'version': '0.1',
    'category': 'Inventory',
    'author': 'Nilar Odoo Dev',
    'license': 'LGPL-3',
    'summary': 'Excel Generate for Barcode',
    'depends': [
        'product',
    ],
    'data': [
        'report/product_label_reports.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
