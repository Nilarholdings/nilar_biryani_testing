# -*- coding: utf-8 -*-
{
    'name': "Account Resequence Access",

    'summary': """Access Right Module for Resequence""",

    'description': """
        This Module Add user access right.
    """,

    'author': "Asia Matrix Software Solution",

    'website': "http://www.asiamatrixsoftware.com",

    'category': 'Security',

    'version': '1.0',

    'license': 'LGPL-3',

    'depends': [
        'account'
    ],

    'data': [
        'security/resequence_action_view.xml',
    ],

    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False,
}
