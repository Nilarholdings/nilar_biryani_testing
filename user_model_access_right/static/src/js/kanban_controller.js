odoo.define('user_model_access_right.ModelAccessRightKanbanController', function (require) {
"use strict";

    var KanbanController = require('web.KanbanController');

    KanbanController.include({
		renderButtons: function ($node) {
			var self = this
			self._super.apply(self, arguments)
			if(!self.$buttons) return

			// Hide Create Button
			self.$buttons.find('.o-kanban-button-new').hide()

			self._rpc({
				model: 'hr.employee',
				method: 'check_model_access_right',
				kwargs: {
					model_name: self.modelName
				}
			}).then(function (res) {
				if (res.can_create) {
					self.$buttons.find('.o-kanban-button-new').show()

				}
			});
		},

    });

});
