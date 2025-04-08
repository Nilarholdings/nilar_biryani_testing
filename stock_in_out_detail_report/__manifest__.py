{
    'name': ' Stock Summary Detail Report',
    'version': '1.6',
    'summary': ' Stock Summary Detail Report',
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
        'reports/stock_detail_excel.xml',
        'wizards/stock_detail_excel_reports.xml',
    ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}