# -*- coding: utf-8 -*-
# Part of Kiran Infosoft. See LICENSE file for full copyright and licensing details.
#
{
    'name': "Multi Employee Login",
    'summary': """Multi Employee Login""",
    'description': """Multi Employee Login""",
    'version': "3.6",
    'category': "website",
    'author': "Kiran Infosoft",
    'website': "http://www.kiraninfosoft.com",
    'license': 'Other proprietary',
    "depends": [
        'base',
        'sale',
        'purchase',
        'account',
        'mrp',
        'hr_expense',
        'stock_requestion',
        'nilar_purchase_requisition',
        'submission_of_quotation',
        'mrp_to_produce',
    ],
    "data": [
        'views/sale_order_view.xml',
        'views/mrp_to_produce_form_view.xml',
    ],
    'application': False,
    'installable': True,
}
