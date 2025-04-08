# -*- coding: utf-8 -*-
{
    'name': 'Custom Menu Extend',
    'version': '0.3',
    'category': 'Extra',
    'sequence': 1001,
    'summary': 'Custom Menu',
    'author': 'nilar',
    'depends': [
        'custom_excel_reports',
        'hr_employee_extend',
        'pos_restaurant',
        'multi_uom',
    ],
    'data': [
        'security/menu_access_groups.xml',
        'views/hr_employee_views.xml',
        'views/product_views.xml',
        'views/pos_views.xml',
        'views/menu_view.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
