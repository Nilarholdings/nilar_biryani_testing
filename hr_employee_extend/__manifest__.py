# -*- coding: utf-8 -*-
{
    'name': "Employee Extend",

    'summary': """Employee Form""",

    'description': """
        1.To Show Warehouse and  ESign Field
    """,

    'author': "nevermore",
    'website': "http://www.blue-stone.net",


    'category': 'hr',
    'version': '1.7',
    'license': "LGPL-3",

    'depends': [
        'base',
        'hr',
        'stock',
        'account_reports',
    ],

    'data': [
        'views/employee_form_view.xml',
        'views/account_bank_statement.xml',

    ],

}
