odoo.define('total_quantity_pos.QuantityChange', function(require) {
    'use strict';

    const OrderSummary = require('point_of_sale.OrderSummary');
    const Registries = require('point_of_sale.Registries');

    const QuantityChange = OrderSummary =>
        class extends OrderSummary {
            //For getting the total items in the product screen
            get total_items() {
                var total_items = this.env.pos.get_order().orderlines.length;
                return total_items;
            }
            //For getting the total count of products in the product screen
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
            get total_without_tax(){
                var total_without_tax = this.env.pos.get_order().get_total_without_tax();
                total_without_tax = this.env.pos.format_currency(total_without_tax)
                return total_without_tax;
            }
        };
    Registries.Component.extend(OrderSummary, QuantityChange);
    return QuantityChange;
});
