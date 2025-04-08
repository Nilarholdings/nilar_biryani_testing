odoo.define('total_quantity_pos.OrderReceiptQty', function(require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt')
    const Registries = require('point_of_sale.Registries');

    const OrderReceiptQty = OrderReceipt =>
        class extends OrderReceipt {
            //For getting the total items in the receipt
            get total_items() {
                var total_items = this.env.pos.get_order().orderlines.length;
                return total_items;
            }
            //For getting the total count of products in the receipt
            get quant_count() {
                var total_items = this.env.pos.get_order().orderlines.length;
                let quant_count = 0;
                let i = 0;
                for (; i < total_items;) {
                    quant_count += this.env.pos.get_order().orderlines.models[i].quantity;
                    i++;
                }
                return quant_count;
            }
            //total without tax
            get total_without_tax() {
                var total_without_tax = this.env.pos.get_order();
                return total_without_tax;
            }
        }
    Registries.Component.extend(OrderReceipt, OrderReceiptQty)
    return OrderReceiptQty
});
