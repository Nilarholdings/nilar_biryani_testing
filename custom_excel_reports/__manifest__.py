# -*- coding: utf-8 -*-

{
    'name': 'Custom Excel Reports',
    'version': '1.3',
    'category': 'Extra',
    'author': 'Nilar Odoo Dev',
    'license': 'LGPL-3',
    'summary': 'Custom Excel Reports',
    'depends': [
        'hr',
        'point_of_sale',
        'stock',
        'base',
        'mail',
        # 'user_access_right',
    ],
    'data': [
        'security/ir.model.access.csv',
        'reports/custom_excel_reports.xml',
        'reports/stock_report_views.xml',
        'reports/stock_received_report_views.xml',
        'reports/menu_items.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
