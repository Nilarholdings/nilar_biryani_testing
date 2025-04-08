{
    'name': 'Sale Summary Report',

    'category': 'sale',

    'description': """
    Sale, Purchase, Invoice and POS analysis report added multi uom and quantity.
    """,

    'author': 'Asia Matrix',

    'version': '2.3',

    'depends': [
        'sale_requisition',
	    'analytic_account',
        'sale_order_extend',
    ],

    'data': [
        'security/ir.model.access.csv',
        'report/sale_summary_report.xml',
        'report/sale_report_extend.xml',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
