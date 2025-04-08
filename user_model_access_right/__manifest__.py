# -*- coding: utf-8 -*-
{
    'name': 'User Access Right on models',
    "author": "Asia Matrix",
    'version': '1.2',
    'license': 'LGPL-3',
    'description': """ 
    User Guideline 
        Step 1 - Employee Access Right must have in User for Model Access Right of Employee Tab
        Step 2 - If access Model Access Right, Employee Access Right must have Related User of this Employee (** Remark- If did not have Employee, Access Right User Error will show).
                Readonly Mode not work in Adminstration User.
        Step 3 - Access right can be given according to the relevant model at Model Access Right.
        
        
        Version 1.0- Model Access Right base on Employee
        Version 1.1- Search Bar add for Model access right lines
     """,
    'depends': [
                    'base', 
                    'web',
                    'purchase',
                    'sale',
                    'account',
                    'stock'
                ],
    'data': [
                'security/ir_model_access.xml',
                'security/ir.model.access.csv',
                'data/data.xml',
                'views/hr_employee_views.xml',
            ],
    'assets': {
        'web.assets_backend': [
            'user_model_access_right/static/src/js/form_controller.js',
            'user_model_access_right/static/src/js/list_controller.js',
            'user_model_access_right/static/src/js/kanban_controller.js',
            'user_model_access_right/static/src/js/basic_view.js',
        ]
    },
    'installable': True,
    'auto_install': False,
    'category': 'Extra Tools',
}
