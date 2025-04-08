# -*- coding: utf-8 -*-
{
    'name': "Button Access Right",

    'summary': """Button Access Right Module""",

    'description': """
        This Module Add button access right.
    """,

    'author': "Nilar Odoo Ddev",

    'website': "http://www.nilarholdings.com",

    'category': 'Security',

    'version': '1.0',

    'license': 'LGPL-3',

    'depends': [
        'sale_requisition',
        'point_of_sale',
        'nilar_purchase_requisition',
        'purchase_requisition',
        'purchase_stock',
        'hr_expense',
        'stock_multi_scrap',
        'repackaging',
        'stock_packaging',
        'mrp',
        'mrp_to_produce',
        'account',
        'account_asset'
    ],

    'data': [
        # Security
        'security/access_group_sales_views.xml',
        'security/access_group_purchase_views.xml',
        'security/access_group_expenses_views.xml',
        'security/access_group_inventory_views.xml',
        'security/access_group_manufacturing_views.xml',
        'security/access_group_accounting_views.xml',

        # Views
        'views/sale_access_views.xml',
        'views/pos_access_views.xml',
        'views/purchase_access_views.xml',
        'views/expenses_access_views.xml',
        'views/inventory_access_views.xml',
        'views/manufacturing_access_views.xml',
        'views/accounting_access_views.xml',

        # Reports
        'reports/button_access_excel_report.xml'
    ],

    'images': ['static/description/icon.png'],
}
