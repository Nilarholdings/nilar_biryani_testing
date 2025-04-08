from odoo import models

class ProductBarcodeReport(models.AbstractModel):
    _name = 'report.barcode_excel.barcode_excel_report'
    _description = 'Product Barcode Excel Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):

        for product in objects:
            sheet_name = product.name
            sheet = workbook.add_worksheet(sheet_name)
            left_style = workbook.add_format({
                'font_name': 'Calibri', 
                'font_size': 25,
                'valign': 'vcenter', 
                'align': 'left', 
                'left': 0,
                'color': 'black', 
            })
            right_style = workbook.add_format({
                'font_name': 'Calibri', 
                'font_size': 25,
                'valign': 'vcenter', 
                'align': 'right', 
                'color': 'black', 
            })
            right_style_bold = workbook.add_format({
                'font_name': 'Calibri', 
                'font_size': 25,
                'valign': 'vcenter', 
                'align': 'right', 
                'right': 0, 
                'color': 'black', 
            })
            product_cell_style_center = workbook.add_format({
                'font_name': 'Calibri', 
                'font_size': 32,
                'valign': 'vcenter', 
                'align': 'center', 
                'right': 0, 
                'bottom' : 0,
                'color': 'black', 
            })
            cell_style_center = workbook.add_format({
                'font_name': 'Calibri', 
                'font_size': 30,
                'valign': 'vcenter', 
                'align': 'center', 
                'right': 0, 
                'bottom' : 0,
                'color': 'black', 
            })
            cell_style_barcode = workbook.add_format({
                'font_name': '3 of 9 Barcode', 
                # 'font_name': 'EAN13', 
                'font_size': 100,
                'valign': 'vcenter', 
                'align': 'center', 
                'right': 0, 
                'color': 'black', 
                'locked': True
            })

            sheet.merge_range(f'A{1}:B{1}', product.name , product_cell_style_center)
            sheet.write('A2', "MFD Date : ", left_style)
            sheet.write('B2', "EXP Date : ", right_style)
            sheet.merge_range(f'A{3}:B{3}', '="*"&A4&"*"', cell_style_barcode)
            sheet.merge_range(f'A{4}:B{4}', str(product.barcode), cell_style_center)
            sheet.write('A5', "Weight : ", left_style)
            sheet.write('B5', "Price : " + str(int(product.list_price)) + " K", right_style_bold)
            sheet.set_column('A:A', 50)
            sheet.set_column('B:B', 50)
            sheet.set_row(0, 70)
            sheet.set_row(1, 50)
            sheet.set_row(2, 130)
            sheet.set_row(3, 50)
            sheet.set_row(4, 50)
