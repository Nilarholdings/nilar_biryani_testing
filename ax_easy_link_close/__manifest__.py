# -*- coding: utf-8 -*-
{
    'name': 'Easy Link Close',
    'version': '1.2',
    'summary': 'AX easy link close module.',
    'description': """
       Some of most used features in one module.
    """,
    'category': 'Setup',
    'website': "www.asiamatrixsoftware.com",
    'email': 'info@asiamatrixsoftware.com',
    'license': "LGPL-3",
    'depends': [
        'sale',
        'sale_order_extend',
        'stock',
        'point_of_sale',
        'analytic_account',
        'pos_restaurant',
        'account',
        'hr_expense',
        'purchase',
        'purchase_requisition',
        'stock',
        'mrp',
        'mrp_to_produce',
    ],
    'data': [
        'views/sale_order_views.xml',
        'views/product_template.xml',
        'views/pos_order_views.xml',
        'views/account_move_views.xml',
        'views/hr_expense_views.xml',
        'views/purchase_order_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_valuation_layer_views.xml',
        'views/stock_move_views.xml',
        'views/mrp_production_views.xml',
        'reports/pos_detail_reports.xml',

    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}
