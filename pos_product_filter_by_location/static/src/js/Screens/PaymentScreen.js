odoo.define('pos_product_filter_by_location.PaymentScreen', function(require){
    'use strict';

    var PaymentScreen = require('point_of_sale.PaymentScreen');
    var Registries = require('point_of_sale.Registries');

    var PaymentScreenExtend = PaymentScreen => class extends PaymentScreen {
    async validateOrder(isForceValidate) {
        var res = await super.validateOrder(...arguments);

        try {
            var lines = this.currentOrder.get_orderlines();

            // Extract product IDs to batch RPC requests
            var productIds = lines.map(line => line.product.id);

            // Batch the check for on-hand quantities for all products in the current order
            var onHandQuantities = await this.env.pos.rpc({
                model: 'pos.order',
                method: 'check_on_hand_qty_batch',
                args: [productIds, this.env.pos.config_id],
            });

            // Update each line's product with the respective quantity
            lines.forEach((line, index) => {
                line.product.onhand_qty = onHandQuantities[index];
            });

            return res;
        } catch (error) {
            console.error('Error in validateOrder:', error);
            return res;
        }
    }
};


    Registries.Component.extend(PaymentScreen, PaymentScreenExtend);

    return PaymentScreenExtend;

});