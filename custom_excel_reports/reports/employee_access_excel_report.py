from odoo import models,fields

class HREmployee(models.Model):
        _inherit = 'hr.employee'

        current_employee_name = fields.Char("Current Employee")

        def name_get(self):
                result = []
                for res in self:
                    if res.current_employee_name:
                        name = res.name + " ("+str(res.current_employee_name)+")"
                    else:
                        name = res.name
                    result.append((res.id, name))
                return result
                
class ResUser(models.Model):
        _inherit = 'res.users'

        def name_get(self):
                result = []
                for res in self:
                    if res.employee_id.current_employee_name:
                        name = res.name + " ("+str(res.employee_id.current_employee_name)+")"
                    else:
                        name = res.name
                    result.append((res.id, name))
                return result

class EmployeeAccessReport(models.AbstractModel):
        _name = 'report.custom_excel_reports.employee_access_excel_report'
        _description = 'Employee Access Excel Report'
        _inherit = 'report.report_xlsx.abstract'

        def generate_xlsx_report(self, workbook, data, objects):
                sheet = workbook.add_worksheet("Employee Access List")

                title_style_center = workbook.add_format({
                        'font_name': 'Calibri', 
                        'font_size': 10,
                        'valign': 'vcenter', 
                        'align': 'center', 
                        'right': 0, 
                        'bottom' : 0,
                        'color': 'black',
                        'border' : 1
                })

                data_style_center = workbook.add_format({
                        'font_name': 'Calibri', 
                        'font_size': 10,
                        'valign': 'vcenter', 
                        'align': 'center', 
                        'right': 0, 
                        'bottom' : 0,
                        'color': 'black',
                        'border' : 1
                })

                data_style_left = workbook.add_format({
                        'font_name': 'Calibri', 
                        'font_size': 10,
                        'valign': 'vcenter', 
                        'align': 'left', 
                        'right': 0, 
                        'bottom' : 0,
                        'color': 'black',
                        'border' : 1
                })

                t_or_f_left_no_b = workbook.add_format({
                        'font_name': 'Wingdings', 
                        'font_size': 15,
                        'valign': 'vcenter', 
                        'align': 'center', 
                        'right': 0, 
                        'bottom' : 0,
                        'border': 1,
                        'color': 'black',
                })

                sheet.set_column('B:B', 40)
                sheet.set_column('C:C', 30)
                sheet.set_column('AD:AE', 30)

                sheet.merge_range(0, 0, 1, 0, "No.", title_style_center)
                sheet.merge_range(0, 1, 1, 1, "Position", data_style_center)
                sheet.merge_range(0, 2, 1, 2, "Current Employee", data_style_center)

                sheet.merge_range(0,3,0,6,"Sales",title_style_center)
                sheet.merge_range(0,7,0,9,"Sale Requisition",title_style_center)
                sheet.merge_range(0,10,0,13,"Purchase Order",title_style_center)
                sheet.merge_range(0,14,0,18,"Purchase Requisition",title_style_center)
                sheet.merge_range(0,19,0,23,"Submission Of Quotation",title_style_center)
                sheet.merge_range(0,24,0,28,"Stock Requisition",title_style_center)
                sheet.merge_range(0,29,0,30,"Stock Requestion Access(User)",title_style_center)

                sheet.write(1,3,"Confirm",title_style_center)
                sheet.write(1,4,"Verify",title_style_center)
                sheet.write(1,5,"Approve",title_style_center)
                sheet.write(1,6,"Cancel",title_style_center)

                sheet.write(1,7,"Confirm",title_style_center)
                sheet.write(1,8,"Approve",title_style_center)
                sheet.write(1,9,"Cancel",title_style_center)

                sheet.write(1,10,"Confirm",title_style_center)
                sheet.write(1,11,"Verified",title_style_center)
                sheet.write(1,12,"Approve",title_style_center)
                sheet.write(1,13,"Cancel",title_style_center)

                sheet.write(1,14,"Confirm",title_style_center)
                sheet.write(1,15,"Verified",title_style_center)
                sheet.write(1,16,"Check",title_style_center)
                sheet.write(1,17,"Approve",title_style_center)
                sheet.write(1,18,"Cancel",title_style_center)

                sheet.write(1,19,"Submit",title_style_center)
                sheet.write(1,20,"Confirm",title_style_center)
                sheet.write(1,21,"Check",title_style_center)
                sheet.write(1,22,"Approve",title_style_center)
                sheet.write(1,23,"Cancel",title_style_center)

                sheet.write(1,24,"Submit",title_style_center)
                sheet.write(1,25,"Confirm",title_style_center)
                sheet.write(1,26,"Check",title_style_center)
                sheet.write(1,27,"Approve",title_style_center)
                sheet.write(1,28,"Cancel",title_style_center)

                sheet.write(1,29,"Approved",title_style_center)
                sheet.write(1,30,"Verified",title_style_center)

                sr_no = 1
                row = 2
                for employee in objects:
                        sheet.write(row,0,sr_no,data_style_center)
                        sheet.write(row,1,employee.name,data_style_left)
                        sheet.write(row,2,employee.current_employee_name or '',data_style_left)
                    
                        # Sales
                        sheet.write(row,3,"=CHAR(252)" if employee.sale_confirm else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,4,"=CHAR(252)" if employee.is_so_verify else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,5,"=CHAR(252)" if employee.is_so_approve else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,6,"=CHAR(252)" if employee.is_so_cancel else "=CHAR(251)",t_or_f_left_no_b)

                        # Sale Requisition Access
                        sheet.write(row,7,"=CHAR(252)" if employee.is_sale_req_confirm else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,8,"=CHAR(252)" if employee.is_sale_req_approve else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,9,"=CHAR(252)" if employee.is_sale_req_cancel else "=CHAR(251)",t_or_f_left_no_b)

                        # Purchase Order Access
                        sheet.write(row,10,"=CHAR(252)" if employee.is_po_confirm else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,11,"=CHAR(252)" if employee.is_po_verified else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,12,"=CHAR(252)" if employee.is_po_approved else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,13,"=CHAR(252)" if employee.is_po_cancel else "=CHAR(251)",t_or_f_left_no_b)

                        # Purchase Requisition Access
                        sheet.write(row,14,"=CHAR(252)" if employee.is_purchase_req_confirm else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,15,"=CHAR(252)" if employee.is_purchase_req_verified else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,16,"=CHAR(252)" if employee.is_purchase_req_checked else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,17,"=CHAR(252)" if employee.is_purchase_req_approved else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,18,"=CHAR(252)" if employee.is_purchase_req_cancel else "=CHAR(251)",t_or_f_left_no_b)

                        # Submission Of Quotation Access
                        sheet.write(row,19,"=CHAR(252)" if employee.is_submit_access else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,20,"=CHAR(252)" if employee.is_confirm_access else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,21,"=CHAR(252)" if employee.is_check_access else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,22,"=CHAR(252)" if employee.is_approve_access else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,23,"=CHAR(252)" if employee.is_cancel_access else "=CHAR(251)",t_or_f_left_no_b)

                        # Stock Requisition Access
                        sheet.write(row,24,"=CHAR(252)" if employee.is_submit_stock_req else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,25,"=CHAR(252)" if employee.is_verified_stock_req else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,26,"=CHAR(252)" if employee.is_approved_stock_req else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,27,"=CHAR(252)" if employee.is_confirm_stock_req else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,28,"=CHAR(252)" if employee.is_cancel_stock_req else "=CHAR(251)",t_or_f_left_no_b)

                        # Stock Requisition Access(User)
                        sheet.write(row,29,"=CHAR(252)" if employee.user_id.has_group('user_access_right.group_approved_access') else "=CHAR(251)",t_or_f_left_no_b)
                        sheet.write(row,30,"=CHAR(252)" if employee.user_id.has_group('user_access_right.group_verified_access') else "=CHAR(251)",t_or_f_left_no_b)

                        row += 1
                        sr_no += 1
