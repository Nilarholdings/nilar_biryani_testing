import pytz
from itertools import groupby
from odoo import api, models, fields
from datetime import datetime

class StockInOutReport(models.AbstractModel):
    _name = 'report.stock_in_out_excel_report.stock_in_out_excel_report'
    _description = 'Stock I/O Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        start_date = data['start_date'] + ' 00:00:00'
        end_date = data['end_date'] + ' 23:59:59'

        sheet = workbook.add_worksheet('Stock In Out Report')
        title_cell = workbook.add_format({
            'font_name': 'Pyidaungsu','font_size': 15, 'text_wrap': True,
            'valign': 'vcenter', 'align': 'center', 'bold': True,
        })
        header_cell = workbook.add_format({
            'font_name': 'Pyidaungsu','bold': True, 'align': 'center', 'font_size': 12, 'valign': 'vcenter', 'text_wrap': True,'bg_color': '#193366','color': '#FFFFFF',
        })
        Location_cell = workbook.add_format({
            'font_name': 'Pyidaungsu','bold': True, 'align': 'left', 'font_size': 12, 'valign': 'vcenter', 'text_wrap': True,
        })

        total_cell = workbook.add_format({
            'font_name': 'Pyidaungsu','bold': True, 'bottom': True, 'top': True, 'align': 'center', 'font_size': 10, 'valign': 'vcenter', 'text_wrap': True,
        })

        left_cell = workbook.add_format({
            'font_name': 'Pyidaungsu','font_size': 10, 'text_wrap': True,
            'valign': 'vcenter', 'align': 'left',
        })
        center_cell = workbook.add_format({
            'font_name': 'Pyidaungsu','font_size': 10, 'text_wrap': True,
            'valign': 'vcenter', 'align': 'center',
        })

        sheet.set_default_row(22)
        blank_row_height = 10
        row_index = 0

        col_sizes = {
            0: 14,
            1: 11,
            2: 40,
            3: 30,
            4: 18,
            5: 14,
            6: 14,
            7: 14,
            8: 14,
        }
        columns = [
					'No.', 'Internal Reference', 'Item', 'Category', 'Family' , 'Opening Qty',
                    'Incoming Qty', 'Outgoing Qty', 'Closing Qty',
                
                    ]

        sheet.set_row(row_index,  26)
        sheet.merge_range(row_index, 0, row_index, 8, self.env.company.name, title_cell)
        row_index += 1
     
        sheet.merge_range(row_index, 0, row_index, 8, 'Stock Summary Report', title_cell)
        row_index += 2

        sheet.merge_range(row_index, 0, row_index, 1, 'Start Date', left_cell)
        sheet.merge_range(row_index, 2, row_index, 4, datetime.strptime(data['start_date'], '%Y-%m-%d').strftime('%d %B, %Y'), left_cell)
        row_index += 1

        sheet.merge_range(row_index, 0, row_index, 1, 'End Date', left_cell)
        sheet.merge_range(row_index, 2, row_index, 4, datetime.strptime(data['end_date'], '%Y-%m-%d').strftime('%d %B, %Y'), left_cell)
        row_index += 1

        sheet.merge_range(row_index, 0, row_index, 1, 'Location', left_cell)
        sheet.merge_range(row_index, 2, row_index, 4, ', '.join(self.env['stock.location'].browse(data['location_ids']).mapped('complete_name')), left_cell)
        row_index += 1

        sheet.set_row(row_index, blank_row_height)
        row_index += 1

        # Datas Header Row
        for index, column_name in enumerate(columns):
            # Adjust column sizes
            sheet.set_column(index, index, col_sizes.get(index, len(column_name) * 1.5))
            sheet.write(row_index, index, column_name, header_cell)

        # row_index += 1
        locations = self.env["stock.location"].search([])
        customer_locations = '(' + ','.join([*map(lambda d: str(d), locations.filtered(lambda l: l.usage == 'customer').ids), '-1', '-2']) + ')'
        vendor_locations = '(' + ','.join([*map(lambda d: str(d), locations.filtered(lambda l: l.usage == 'supplier').ids), '-1', '-2']) + ')'
        scrap_locations = '(' + ','.join([*map(lambda d: str(d), locations.filtered(lambda l: l.usage == 'inventory' and l.scrap_location).ids), '-1', '-2']) + ')'
        adjustment_locations = '(' + ','.join([*map(lambda d: str(d), locations.filtered(lambda l: l.usage == 'inventory' and not l.scrap_location).ids), '-1', '-2']) + ')'
        internal_locations_ids = locations.filtered(lambda l: l.usage == 'internal' and not l.scrap_location).ids
        internal_locations = '(' + ','.join([*map(lambda d: str(d), internal_locations_ids), '-1', '-2']) + ')'
        production_locations = '(' + ','.join([*map(lambda d: str(d), locations.filtered(lambda l: l.usage == 'production').ids), '-1', '-2']) + ')'
        unpacking_locations = '(' + ','.join([*map(lambda d: str(d), locations.filtered(lambda l: l.usage == 'unpackaging').ids), '-1', '-2']) + ')'


        location_ids = data['location_ids']
        if not location_ids: location_ids = internal_locations_ids

        product_ids = data['product_ids']
        def filter_query(req_query):
            # Filter datas base on user choices
            if location_ids:
                location_ids_str = '(' + ','.join(map(str, location_ids)) + ')'
                req_query += f"""
                    And (sml.location_id in {location_ids_str} or sml.location_dest_id in {location_ids_str}) 
                """

            if product_ids:
                product_ids_str = '(' + ','.join(map(str, product_ids)) + ')'
                req_query += f"""
                    And sml.product_id in {product_ids_str}
                """
            return req_query 

        select_query = """
                    -- IN / out Moves
                    SELECT  sml.product_id,
                            sml.date::varchar,

                            sml.location_id,
                            sml.location_dest_id,
                            
                            sml.qty_done as qty,
                            sm.product_uom_qty as qty,

                            -- Sale Qty
                            case 
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sm.sale_line_id is not null and  sml.location_dest_id in {customer_locations} then sml.qty_done
                                else 0
                            end as sale_qty,
                            
                            -- Sale Return Qty
                            case 
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sm.sale_line_id is not null and sml.location_id in {customer_locations} then sml.qty_done
                                else 0
                            end as sale_return_qty,

                            -- Purchase Qty 
                            case 
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sm.purchase_line_id is not null and sml.location_id in {vendor_locations} then sml.qty_done                
                                else 0
                            end as purchase_qty,

                            -- Purchase Return Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sm.purchase_line_id is not null and sml.location_dest_id in {vendor_locations} then sml.qty_done
                                else 0
                            end as purchase_return_qty,

                            -- Receive In Qty ( From Replenishment )
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND (sm.orderpoint_id is not null or sl.usage = 'transit')  AND sml.location_dest_id in {internal_locations} then sml.qty_done
                                else 0
                            end as receive_in_qty,
                    
                            -- Deliver Out Qty ( From Replenishment )
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND (sm.orderpoint_id is not null or dl.usage='transit') AND sml.location_id in {internal_locations} then sml.qty_done
                                else 0
                            end as deliver_out_qty,

                            -- POS Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sp.pos_order_id is not null AND sml.location_dest_id in {customer_locations} then sml.qty_done
                                else 0
                            end as pos_qty,

                            -- POS Return Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sp.pos_order_id is not null AND sml.location_id in {customer_locations} then sml.qty_done
                                else 0
                            end as pos_return_qty,
                    
                            -- Receive Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sp.pos_order_id is null AND sm.purchase_line_id is null AND sml.location_id in {vendor_locations} then sml.qty_done
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sp.pos_order_id is null AND sm.purchase_line_id is null AND sml.location_dest_id in {vendor_locations} then -sml.qty_done
                                else 0
                            end as receive_qty,
                    
                            -- Delivery Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sp.pos_order_id is null AND sm.sale_line_id is null AND sml.location_dest_id in {customer_locations} then sml.qty_done
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sp.pos_order_id is null AND sm.sale_line_id is null AND sml.location_id in {customer_locations} then -sml.qty_done
                                else 0
                            end as deliver_qty,
                            
                            -- internal_transfer_in_or_out_qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sml.location_id in {internal_locations} AND sml.location_dest_id in {internal_locations} then sml.qty_done
                                else 0
                            end as transfer_qty,
                            
                            -- ADJ Qty  
                            case 
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND  sml.location_dest_id in {adjustment_locations} then sml.qty_done
                
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND sml.location_id in {adjustment_locations} then sml.qty_done
                                else 0
                            end as adjustment_qty,

                            -- Scrap Qty    
                            case 
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND  sml.location_dest_id in {scrap_locations} then sml.qty_done
                                else 0
                            end as scrap_qty,

                            case 
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}' AND  sml.location_dest_id in {scrap_locations} then sml.qty_done
                                else 0
                            end as scrap_qty,

                            -- production Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sm.raw_material_production_id is not null AND sml.location_dest_id in {production_locations} then sm.product_uom_qty
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sm.production_id is not null AND sml.location_id in {production_locations} then sm.product_uom_qty
                                else 0
                            end as production_qty,

                            -- unbuild Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sm.unbuild_id is not null AND sml.location_dest_id in {production_locations} then sm.product_uom_qty
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sm.unbuild_id is not null AND sml.location_id in {production_locations} then sm.product_uom_qty
                                else 0
                            end as unbuild_qty,

                            -- good received Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sm.purchase_line_id is not null AND sml.location_dest_id in {internal_locations} then sml.qty_done
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sm.purchase_line_id is not null AND sml.location_id in {internal_locations} then -sml.qty_done
                                else 0
                            end as good_received_qty,

                            -- Unpackaging Qty
                            case
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sml.location_dest_id in {unpacking_locations} then sml.qty_done
                                when SML.DATE >= '{start_date}' AND SML.DATE <= '{end_date}'  AND sml.location_id in {unpacking_locations} then sml.qty_done
                                else 0
                            end as unpackaging_qty

                    FROM        STOCK_MOVE_LINE SML
                    LEFT JOIN   STOCK_MOVE SM ON SM.ID=SML.MOVE_ID
                    LEFT JOIN   STOCK_PICKING SP ON SP.ID = SM.PICKING_ID
                    LEFT JOIN   STOCK_LOCATION SL ON SL.ID = SML.LOCATION_ID
                    LEFT JOIN   STOCK_LOCATION DL ON DL.ID = SML.LOCATION_DEST_ID
                    LEFT JOIN PRODUCT_PRODUCT PP ON PP.ID=SM.PRODUCT_ID
                    LEFT JOIN PRODUCT_TEMPLATE PT ON PT.ID=PP.PRODUCT_TMPL_ID
       
                    WHERE       sml.state in ('done') and
                                SML.DATE < '{end_date}'

        """       
        select_query = filter_query(select_query)

        transactions_query = (select_query).format(
            start_date = start_date,
            end_date = end_date,
            customer_locations = customer_locations,
            vendor_locations = vendor_locations,
            scrap_locations = scrap_locations,
            adjustment_locations = adjustment_locations,
            internal_locations = internal_locations,
            production_locations = production_locations,
            unpacking_locations = unpacking_locations,

        )
        self.env.cr.execute(transactions_query)
        transactions_result = self.env.cr.dictfetchall()
        transactions_result_products = list(set([r['product_id'] for r in transactions_result]))
        

        for location_id in location_ids:
            result_for_location = list(filter(lambda r: r['location_id'] == location_id or r['location_dest_id'] == location_id, transactions_result))
            if not result_for_location: continue

            location = self.env['stock.location'].browse(location_id)
            total_deliver_qty = total_receive_qty = total_sale_qty = total_sale_return_qty = total_purchase_qty = total_purchase_return_qty = total_pos_qty = total_pos_return_qty = total_receive_in_qty = total_deliver_out_qty = total_internal_transfer_qty_in = total_internal_transfer_qty_out = total_scrap_qty = total_opening_qty = total_closing_qty = total_incoming_qty = total_outgoing_qty = total_production_in_qty = total_production_out_qty = total_unbuild_in_qty = total_unbuild_out_qty = total_good_received_qty = total_adjustment_qty_in = total_adjustment_qty_out = total_unpackaging_qty_in = total_unpackaging_qty_out = 0
            row_number = 1
            row_index_for_total = row_index
            row_index += 1
            col_index = 0

            # if any([total_opening_qty, total_incoming_qty, total_outgoing_qty , total_closing_qty, ]): 
            sheet.write(row_index, col_index ,  location.complete_name, Location_cell)
            row_index += 1
            for product_id, records in groupby(sorted(result_for_location, key = lambda l: l['product_id']), lambda l: l['product_id']):
                records_list = list(records)
                
                product = self.env['product.product'].browse(product_id)
                opening_records = list(filter(lambda l: l['date'] < start_date, records_list))
                opening_qty = sum([i['qty'] for i in list(filter(lambda l: l['location_dest_id'] == location_id, opening_records))]) - sum([i['qty'] for i in list(filter(lambda l: l['location_id'] == location_id, opening_records))]) 
                remaing_list = [i for i in records_list if i not in opening_records]

                sale_qty = sum([i['sale_qty'] for i in remaing_list])
                sale_return_qty = sum([i['sale_return_qty'] for i in remaing_list])
                purchase_qty = sum([i['purchase_qty'] for i in remaing_list])
                purchase_return_qty = sum([i['purchase_return_qty'] for i in remaing_list])
                receive_in_qty = sum([i['receive_in_qty'] for i in remaing_list])
                deliver_out_qty = sum([i['deliver_out_qty'] for i in remaing_list])
                pos_qty = sum([i['pos_qty'] for i in remaing_list])
                pos_return_qty = sum([i['pos_return_qty'] for i in remaing_list])
                receive_qty = sum([i['receive_qty'] for i in remaing_list])
                deliver_qty = sum([i['deliver_qty'] for i in remaing_list])
                internal_transfer_in_qty = sum([i['transfer_qty'] if i['location_dest_id'] == location_id else 0 for i in remaing_list]) 
                internal_transfer_out_qty = sum([i['transfer_qty'] if i['location_id'] == location_id else 0 for i in remaing_list]) 
                adjustment_in_qty = sum([i['adjustment_qty'] if i['location_dest_id'] == location_id else 0 for i in remaing_list]) 
                adjustment_out_qty = sum([i['adjustment_qty'] if i['location_id'] == location_id else 0 for i in remaing_list]) 
                unpackaging_out_qty = sum([i['unpackaging_qty'] if i['location_dest_id'] == location_id else 0 for i in remaing_list]) 
                unpackaging_in_qty = sum([i['unpackaging_qty'] if i['location_id'] == location_id else 0 for i in remaing_list]) 
                # adjustment_qty = sum([i['adjustment_qty'] for i in remaing_list])
                scrap_qty = sum([i['scrap_qty'] for i in remaing_list])
                production_in_qty = sum([i['production_qty'] if i['location_dest_id'] == location_id else 0 for i in remaing_list])
                production_out_qty = sum([i['production_qty'] if i['location_id'] == location_id else 0 for i in remaing_list])
                # unbuild_qty = sum([i['unbuild_qty'] for i in remaing_list])
                unbuild_out_qty = sum([i['unbuild_qty'] if i['location_dest_id'] == location_id else 0 for i in remaing_list])
                unbuild_in_qty = sum([i['unbuild_qty'] if i['location_id'] == location_id else 0 for i in remaing_list])
                good_received_qty = sum([i['good_received_qty'] for i in remaing_list])
                incoming_qty =  internal_transfer_in_qty + sale_return_qty + purchase_qty + receive_in_qty + pos_return_qty + receive_qty + adjustment_in_qty + unpackaging_in_qty + production_in_qty + unbuild_out_qty
                outgoing_qty = internal_transfer_out_qty + deliver_qty + pos_qty + sale_qty + purchase_return_qty + deliver_out_qty + scrap_qty + adjustment_out_qty + unpackaging_out_qty + production_out_qty + unbuild_in_qty
                closing_qty = (opening_qty) + (internal_transfer_in_qty + sale_return_qty + purchase_qty + receive_in_qty + pos_return_qty + receive_qty + production_in_qty + adjustment_in_qty + unpackaging_in_qty + unbuild_out_qty ) - (internal_transfer_out_qty + deliver_qty + pos_qty + sale_qty + purchase_return_qty + deliver_out_qty + scrap_qty + adjustment_out_qty + unpackaging_out_qty + production_out_qty + unbuild_in_qty )

                if any([opening_qty, incoming_qty, outgoing_qty , closing_qty, ]):    
                    
                    col_index = 0
                    sheet.write(row_index, col_index, row_number, center_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, product.default_code or '', left_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, product.name, left_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, product.categ_id.complete_name or '', left_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, product.product_family_id.name or '', left_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, opening_qty, center_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, incoming_qty, center_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, outgoing_qty, center_cell)
                    col_index += 1
                    sheet.write(row_index, col_index, closing_qty, center_cell)
                    col_index += 1
                    # sheet.write(row_index, col_index, production_qty, center_cell)
                    # col_index += 1
                    # sheet.write(row_index, col_index, unbuild_qty, center_cell)
                    # col_index += 1
                    # sheet.write(row_index, col_index, good_received_qty, center_cell)
                    # col_index += 1
                    # sheet.write(row_index, col_index, repackaging_quantity, center_cell)
                    # col_index += 1
                    # sheet.write(row_index, col_index, unpackaging_quantity, center_cell)
                    # col_index += 1

                    total_opening_qty += opening_qty
                    total_purchase_qty += purchase_qty
                    total_purchase_return_qty += purchase_return_qty
                    total_sale_qty += sale_qty
                    total_sale_return_qty += sale_return_qty
                    total_pos_qty += pos_qty
                    total_pos_return_qty += pos_return_qty
                    total_deliver_qty += deliver_qty
                    total_receive_qty += receive_qty
                    total_internal_transfer_qty_in += internal_transfer_in_qty
                    total_internal_transfer_qty_out += internal_transfer_out_qty
                    total_adjustment_qty_in += adjustment_in_qty
                    total_adjustment_qty_out += adjustment_out_qty
                    total_unpackaging_qty_in += unpackaging_in_qty
                    total_unpackaging_qty_out += unpackaging_out_qty
                    total_scrap_qty += scrap_qty
                    total_receive_in_qty += receive_in_qty
                    total_deliver_out_qty += deliver_out_qty
                    total_incoming_qty += incoming_qty
                    total_outgoing_qty += outgoing_qty
                    total_production_in_qty += production_in_qty
                    total_production_out_qty += production_out_qty
                    total_unbuild_in_qty += unbuild_in_qty
                    total_unbuild_out_qty += unbuild_out_qty
                    total_closing_qty += closing_qty
                    total_good_received_qty += good_received_qty
                    row_number += 1
                    row_index += 1

            if any([total_opening_qty, total_incoming_qty, total_outgoing_qty , total_closing_qty, ]):        

                sheet.merge_range(row_index, 0, row_index, 4, 'Total', total_cell)
                col_index = 5
                sheet.write(row_index, col_index, total_opening_qty, total_cell)
                col_index += 1
                sheet.write(row_index, col_index, total_incoming_qty, total_cell)
                col_index += 1
                sheet.write(row_index, col_index, total_outgoing_qty, total_cell)
                col_index += 1
                sheet.write(row_index, col_index, total_closing_qty, total_cell)
                col_index += 1
                row_index += 1
            
            #     col_index = 0
            #     sheet.write(row_index, col_index ,  location.complete_name, Location_cell)
            #     row_index += 1
            # # sheet.set_row(row_index, blank_row_height)
            # row_index += 1

               

          

              

          

