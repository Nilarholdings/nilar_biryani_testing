odoo.define('user_model_access_right.BasicView', function (require) {
"use strict";

    var BasicView = require('web.BasicView');
    var rpc = require('web.rpc');

    BasicView.include({
        init: function(viewInfo, params) {
            var self = this;
            this._super.apply(this, arguments);

            rpc.query({
				model: 'hr.employee',
				method: 'check_model_access_right',
				kwargs: {
					model_name: self.controllerParams.modelName
				}
			}).then(function (res) {
				if ([false, null, undefined].includes(res.can_delete))  {
					self.controllerParams.activeActions.delete = false
				}

			});
        },
    });
});
