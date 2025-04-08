# -*- coding: utf-8 -*-
{
    'name': "All Report Templates",
    'summary': """
        All report templates""",
    'description': """
        Templates for Sales,Purchase,Invoice and Inventory
    """,
    'author': "znl",
    'website': "http://www.asiamatrixsoftware.com",
    'category': 'Report',
    'version': '5.5',
    'depends': [
        'web',
        'sale',
        'purchase',
        'report_py3o',
        'account',
        'submission_of_quotation',
        'hr_expense',
        'report_qweb_element_page_visibility',
        'stock_requestion',
        'nilar_purchase_requisition',
        'stock_multi_scrap',

    ],
    'data': [
        'data/sequence_code.xml',
        'views/account_bank_statement.xml',
        'report/expense_pdf_inherit.xml',
        'report/production_pdf_inherit.xml',
        'report/report.xml',
        'report/invoive_pdf_inherit.xml',

    ],
    'license': 'LGPL-3',
}
