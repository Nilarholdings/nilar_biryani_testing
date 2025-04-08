{
    'name': ' Stock Summary Report',
    'version': '1.1',
    'summary': ' Stock Summary Report',
    'description': """
    
    """,
    'category': 'Setup',
    'website': "",
    'email': '',
    'license': "LGPL-3",
    'depends': [
        'sale_stock',
        'purchase_stock',
        'report_xlsx',
   
    ],
    'data': [        
        'security/ir.model.access.csv',
        'reports/stock_excel.xml',
        'wizards/stock_excel_reports.xml',
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}