from odoo import models,fields

class EmployeeAccessReport(models.AbstractModel):
        _name = 'report.odoo_button_access_right.button_access_excel_report'
        _description = 'Button Access Excel Report'
        _inherit = 'report.report_xlsx.abstract'

        def generate_xlsx_report(self, workbook, data, objects):
                sheet1 = workbook.add_worksheet("(Sale+POS+Purchase+Expense)")
                sheet2 = workbook.add_worksheet("(Inventory+Manufacturing)")
                sheet3 = workbook.add_worksheet("(Accounting)")

                user = objects[0]

                title_style_center = workbook.add_format({
                        'font_name': 'Calibri', 
                        'font_size': 10,
                        'valign': 'vcenter', 
                        'align': 'center', 
                        'right': 0, 
                        'bottom' : 0,
                        'color': 'black',
                        'border' : 1,
                        'bold': True
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
                normal_data_style_center = workbook.add_format({
                        'font_name': 'Calibri', 
                        'font_size': 10,
                        'valign': 'vcenter', 
                        'align': 'center', 
                        'right': 0, 
                        'bottom' : 0,
                        'color': 'black'
                })
                normal_data_style_left = workbook.add_format({
                        'font_name': 'Calibri', 
                        'font_size': 10,
                        'valign': 'vcenter', 
                        'align': 'left', 
                        'right': 0, 
                        'bottom' : 0,
                        'color': 'black'
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

                sheet1.set_column('A:A', 30)
                sheet1.set_column('B:B', 25)
                sheet1.set_column('C:C', 20)
                sheet1.set_column('D:D', 60)
                sheet2.set_column('A:A', 30)
                sheet2.set_column('B:B', 25)
                sheet2.set_column('C:C', 20)
                sheet2.set_column('D:D', 60)
                sheet3.set_column('A:A', 30)
                sheet3.set_column('B:B', 25)
                sheet3.set_column('C:C', 20)
                sheet3.set_column('D:D', 60)

                row_num = 0
                while row_num < 33:
                        sheet1.set_row(row_num,30)
                        sheet2.set_row(row_num,30)
                        sheet3.set_row(row_num,30)
                        row_num += 1

                sheet1.merge_range(0,0,0,3,"Nilar Biryani Co.,Ltd",title_style_center)
                sheet2.merge_range(0,0,0,3,"Nilar Biryani Co.,Ltd",title_style_center)
                sheet3.merge_range(0,0,0,3,"Nilar Biryani Co.,Ltd",title_style_center)

                sheet1.merge_range(1,0,1,3,"Odoo Software's  Employee Access Right",title_style_center)
                sheet2.merge_range(1,0,1,3,"Odoo Software's  Employee Access Right",title_style_center)
                sheet3.merge_range(1,0,1,3,"Odoo Software's  Employee Access Right",title_style_center)

                sheet1.write(2,0,"Employee Name",normal_data_style_center)
                sheet1.write(2,1,user.employee_id.current_employee_name,normal_data_style_left)
                sheet1.write(3,0,"Employee Position",normal_data_style_center)
                sheet1.write(3,1,user.name,normal_data_style_left)
                sheet2.write(2,0,"Employee Name",normal_data_style_center)
                sheet2.write(2,1,user.employee_id.current_employee_name,normal_data_style_left)
                sheet2.write(3,0,"Employee Position",normal_data_style_center)
                sheet2.write(3,1,user.name,normal_data_style_left)
                sheet3.write(2,0,"Employee Name",normal_data_style_center)
                sheet3.write(2,1,user.employee_id.current_employee_name,normal_data_style_left)
                sheet3.write(3,0,"Employee Position",normal_data_style_center)
                sheet3.write(3,1,user.name,normal_data_style_left)

                sheet1.write(2,3,"Date :",normal_data_style_center)
                sheet2.write(2,3,"Date :",normal_data_style_center)
                sheet3.write(2,3,"Date :",normal_data_style_center)

                sheet1.write(5,0,"Description",title_style_center)
                sheet1.write(5,1,"Button",title_style_center)
                sheet1.write(5,2,"Allow or Disallow",title_style_center)
                sheet1.write(5,3,"Remark",title_style_center)
                sheet2.write(5,0,"Description",title_style_center)
                sheet2.write(5,1,"Button",title_style_center)
                sheet2.write(5,2,"Allow or Disallow",title_style_center)
                sheet2.write(5,3,"Remark",title_style_center)
                sheet3.write(5,0,"Description",title_style_center)
                sheet3.write(5,1,"Button",title_style_center)
                sheet3.write(5,2,"Allow or Disallow",title_style_center)
                sheet3.write(5,3,"Remark",title_style_center)

                # For Sheet1 Sale+POS+Purchase+Expense
                sheet1.merge_range(6, 0, 9, 0, "WholeSales Requisition", data_style_center)
                sheet1.write(6,1,"Create Invoice",data_style_center)
                sheet1.write(7,1,"Create Requisition",data_style_center)
                sheet1.write(8,1,"Sent to Quotation",data_style_center)
                sheet1.write(9,1,"Send by Email",data_style_center)
                sheet1.write(6,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_create_invoice_access_ws') else "",t_or_f_left_no_b)
                sheet1.write(7,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_create_requisition_access_ws') else "",t_or_f_left_no_b)
                sheet1.write(8,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_sent_to_quotation_access_ws') else "",t_or_f_left_no_b)
                sheet1.write(9,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_sent_by_email_access_ws') else "",t_or_f_left_no_b)

                sheet1.write(10,0,"Retail Sale Requisition", data_style_center)
                sheet1.write(10,1,"Reset to Confirm",data_style_center)
                sheet1.write(10,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_to_confirm_access_rs') else "",t_or_f_left_no_b)

                sheet1.merge_range(11,0,12,0,"Point of Sales Order",data_style_center)
                sheet1.write(11,1,"Invoice",data_style_center)
                sheet1.write(12,1,"Return Products",data_style_center)
                sheet1.write(11,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_invoice_pos_access_ws') else "",t_or_f_left_no_b)
                sheet1.write(12,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_return_products_pos_access_ws') else "",t_or_f_left_no_b)

                sheet1.merge_range(13,0,18,0,"Purchase Order",data_style_center)
                sheet1.write(13,1,"Sent by Mail",data_style_center)
                sheet1.write(14,1,"Set to Draft",data_style_center)
                sheet1.write(15,1,"Lock/Unlock",data_style_center)
                sheet1.write(16,1,"Sent PO by Mail",data_style_center)
                sheet1.write(17,1,"Receive Products",data_style_center)
                sheet1.write(18,1,"Create Bill",data_style_center)
                sheet1.write(13,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_send_by_mail_access_po') else "",t_or_f_left_no_b)
                sheet1.write(14,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_set_to_draft_access_po') else "",t_or_f_left_no_b)
                sheet1.write(15,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_lock_unlock_access_po') else "",t_or_f_left_no_b)
                sheet1.write(16,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_send_by_mail_access_po') else "",t_or_f_left_no_b)
                sheet1.write(17,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_receive_products_access_po') else "",t_or_f_left_no_b)
                sheet1.write(18,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_create_bill_access_po') else "",t_or_f_left_no_b)

                sheet1.write(19,0,"Purchase Requisition Detail",data_style_center)
                sheet1.write(19,1,"Create Purchase Agreement",data_style_center)
                sheet1.write(19,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_create_purchase_agg_access_pr') else "",t_or_f_left_no_b)

                sheet1.merge_range(20,0,22,0,"Purchase Agreement",data_style_center)
                sheet1.write(20,1,"Confirm",data_style_center)
                sheet1.write(21,1,"Cancel",data_style_center)
                sheet1.write(22,1,"Reset to Draft",data_style_center)
                sheet1.write(20,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_confirm_access_pa') else "",t_or_f_left_no_b)
                sheet1.write(21,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_cancel_access_pa') else "",t_or_f_left_no_b)
                sheet1.write(22,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_to_draft_access_pa') else "",t_or_f_left_no_b)

                sheet1.merge_range(23,0,25,0,"Expenses",data_style_center)
                sheet1.write(23,1,"Attach Receipt",data_style_center)
                sheet1.write(24,1,"Create Report",data_style_center)
                sheet1.write(25,1,"View Report",data_style_center)
                sheet1.write(23,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_attach_receipt_access_expense') else "",t_or_f_left_no_b)
                sheet1.write(24,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_create_report_access_expense') else "",t_or_f_left_no_b)
                sheet1.write(25,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_view_report_access_expense') else "",t_or_f_left_no_b)

                sheet1.merge_range(26,0,32,0,"Expenses Reports",data_style_center)
                sheet1.write(26,1,"Submit to Manager",data_style_center)
                sheet1.write(27,1,"Approve",data_style_center)
                sheet1.write(28,1,"Refuse",data_style_center)
                sheet1.write(29,1,"Reset to Draft",data_style_center)
                sheet1.write(30,1,"Post Journal Entries",data_style_center)
                sheet1.write(31,1,"Register Payment",data_style_center)
                sheet1.write(32,1,"Cancel",data_style_center)
                sheet1.write(26,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_submit_mgr_access_expense_report') else "",t_or_f_left_no_b)
                sheet1.write(27,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_approve_access_expense_report') else "",t_or_f_left_no_b)
                sheet1.write(28,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_refuse_access_expense_report') else "",t_or_f_left_no_b)
                sheet1.write(29,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_access_expense_report') else "",t_or_f_left_no_b)
                sheet1.write(30,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_post_journal_access_expense_report') else "",t_or_f_left_no_b)
                sheet1.write(31,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_register_payment_access_expense_report') else "",t_or_f_left_no_b)
                sheet1.write(32,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_cancel_access_expense_report') else "",t_or_f_left_no_b)

                # For Sheet2 inventory+Manufacturing
                sheet2.merge_range(6,0,12,0,"Transfer/Received/Issued",data_style_center)
                sheet2.write(6,1,"Cancel",data_style_center)
                sheet2.write(7,1,"Mark as To Do",data_style_center)
                sheet2.write(8,1,"Lock/Unlock",data_style_center)
                sheet2.write(9,1,"Set Quantities",data_style_center)
                sheet2.write(10,1,"Validate",data_style_center)
                sheet2.write(11,1,"Put in Back",data_style_center)
                sheet2.write(12,1,"Return",data_style_center)
                sheet2.write(6,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_cancel_access_transfer') else "",t_or_f_left_no_b)
                sheet2.write(7,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_mark_as_to_do_access_transfer') else "",t_or_f_left_no_b)
                sheet2.write(8,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_lock_unlock_access_transfer') else "",t_or_f_left_no_b)
                sheet2.write(9,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_set_quantities_access_transfer') else "",t_or_f_left_no_b)
                sheet2.write(10,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_validate_access_transfer') else "",t_or_f_left_no_b)
                sheet2.write(11,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_put_in_pack_access_transfer') else "",t_or_f_left_no_b)
                sheet2.write(12,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_return_access_transfer') else "",t_or_f_left_no_b)

                sheet2.merge_range(13,0,15,0,"Inventory Adjusment",data_style_center)
                sheet2.write(13,1,"Apply",data_style_center)
                sheet2.write(14,1,"Clear",data_style_center)
                sheet2.write(15,1,"Request a Count",data_style_center)
                sheet2.write(13,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_apply_access_adjustment') else "",t_or_f_left_no_b)
                sheet2.write(14,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_clear_access_adjustment') else "",t_or_f_left_no_b)
                sheet2.write(15,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_request_a_count_access_adjustment') else "",t_or_f_left_no_b)

                sheet2.write(16,0,"Multi Scrap",data_style_center)
                sheet2.write(16,1,"Validate",data_style_center)
                sheet2.write(16,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_validate_access_multi_scrap') else "",t_or_f_left_no_b)

                sheet2.merge_range(17,0,19,0,"Unpacking(Big->Small)",data_style_center)
                sheet2.write(17,1,"Repackage",data_style_center)
                sheet2.write(18,1,"Validate",data_style_center)
                sheet2.write(19,1,"Reset to Draft",data_style_center)
                sheet2.write(17,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_repackage_access_unpacking') else "",t_or_f_left_no_b)
                sheet2.write(18,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_validate_access_unpacking') else "",t_or_f_left_no_b)
                sheet2.write(19,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_access_unpacking') else "",t_or_f_left_no_b)

                sheet2.merge_range(20,0,22,0,"Packing(Small->Big)",data_style_center)
                sheet2.write(20,1,"Package",data_style_center)
                sheet2.write(21,1,"Reset to Draft",data_style_center)
                sheet2.write(22,1,"Validate",data_style_center)
                sheet2.write(20,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_package_access_packing') else "",t_or_f_left_no_b)
                sheet2.write(21,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_access_packing') else "",t_or_f_left_no_b)
                sheet2.write(22,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_validate_access_packing') else "",t_or_f_left_no_b)

                sheet2.write(23,0,"Stock Requisition",data_style_center)
                sheet2.write(23,1,"Set to Verified",data_style_center)
                sheet2.write(23,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_set_to_verified_access_sr') else "",t_or_f_left_no_b)

                sheet2.merge_range(24,0,30,0,"Manufacturing Order",data_style_center)
                sheet2.write(24,1,"confirm",data_style_center)
                sheet2.write(25,1,"Create MO Produce",data_style_center)
                sheet2.write(26,1,"Mark as Done",data_style_center)
                sheet2.write(27,1,"Unreserve",data_style_center)
                sheet2.write(28,1,"Lock/Unlock",data_style_center)
                sheet2.write(29,1,"Unbuild",data_style_center)
                sheet2.write(30,1,"Cancel",data_style_center)
                sheet2.write(24,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_confirm_access_mo') else "",t_or_f_left_no_b)
                sheet2.write(25,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_create_mo_produce_access_mo') else "",t_or_f_left_no_b)
                sheet2.write(26,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_mark_as_done_access_mo') else "",t_or_f_left_no_b)
                sheet2.write(27,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_unreserve_access_mo') else "",t_or_f_left_no_b)
                sheet2.write(28,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_lock_unlock_access_mo') else "",t_or_f_left_no_b)
                sheet2.write(29,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_unbuild_access_mo') else "",t_or_f_left_no_b)
                sheet2.write(30,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_cancel_access_mo') else "",t_or_f_left_no_b)

                sheet2.write(31,0,"Manufacturing Order to Product",data_style_center)
                sheet2.write(31,1,"Confirm",data_style_center)
                sheet2.write(31,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_confirm_access_mo_product') else "",t_or_f_left_no_b)

                # For Sheet3 Accounting
                sheet3.merge_range(6,0,10,0,"Invoices/Credit Notes/Bill/Refunds",data_style_center)
                sheet3.write(6,1,"Confirm",data_style_center)
                sheet3.write(7,1,"Cancel",data_style_center)
                sheet3.write(8,1,"Reset to Draft",data_style_center)
                sheet3.write(9,1,"Register Payment",data_style_center)
                sheet3.write(10,1,"Add Credit Note",data_style_center)
                sheet3.write(6,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_confirm_access_accounting') else "",t_or_f_left_no_b)
                sheet3.write(7,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_cancel_access_accounting') else "",t_or_f_left_no_b)
                sheet3.write(8,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_access_accounting') else "",t_or_f_left_no_b)
                sheet3.write(9,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_register_payment_access_accounting') else "",t_or_f_left_no_b)
                sheet3.write(10,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_credit_note_access_accounting') else "",t_or_f_left_no_b)

                sheet3.merge_range(11,0,13,0,"Payments",data_style_center)
                sheet3.write(11,1,"Confirm",data_style_center)
                sheet3.write(12,1,"Cancel",data_style_center)
                sheet3.write(13,1,"Reset to Draft",data_style_center)
                sheet3.write(11,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_confirm_access_payment') else "",t_or_f_left_no_b)
                sheet3.write(12,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_cancel_access_payment') else "",t_or_f_left_no_b)
                sheet3.write(13,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_access_payment') else "",t_or_f_left_no_b)

                sheet3.merge_range(14,0,17,0,"Jounal Entries",data_style_center)
                sheet3.write(14,1,"Post",data_style_center)
                sheet3.write(15,1,"Cancel Entry",data_style_center)
                sheet3.write(16,1,"Reset to Draft",data_style_center)
                sheet3.write(17,1,"Reverse Entry",data_style_center)
                sheet3.write(14,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_post_access_je') else "",t_or_f_left_no_b)
                sheet3.write(15,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_cancel_access_je') else "",t_or_f_left_no_b)
                sheet3.write(16,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_access_je') else "",t_or_f_left_no_b)
                sheet3.write(17,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reverse_access_je') else "",t_or_f_left_no_b)

                sheet3.merge_range(18,0,24,0,"Assets",data_style_center)
                sheet3.write(18,1,"Confirm",data_style_center)
                sheet3.write(19,1,"Compute Depreciation",data_style_center)
                sheet3.write(20,1,"Sell or Dispose",data_style_center)
                sheet3.write(21,1,"Pause Depreciation",data_style_center)
                sheet3.write(22,1,"Modify Depreciation",data_style_center)
                sheet3.write(23,1,"Save Model",data_style_center)
                sheet3.write(24,1,"Set to Draft",data_style_center)
                sheet3.write(18,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_confirm_access_assets') else "",t_or_f_left_no_b)
                sheet3.write(19,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_compute_depre_access_assets') else "",t_or_f_left_no_b)
                sheet3.write(20,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_sell_dispose_access_assets') else "",t_or_f_left_no_b)
                sheet3.write(21,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_pause_depre_access_assets') else "",t_or_f_left_no_b)
                sheet3.write(22,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_modify_depre_access_assets') else "",t_or_f_left_no_b)
                sheet3.write(23,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_save_model_access_assets') else "",t_or_f_left_no_b)
                sheet3.write(24,2,"=CHAR(252)" if user.has_group('odoo_button_access_right.group_reset_access_assets') else "",t_or_f_left_no_b)


