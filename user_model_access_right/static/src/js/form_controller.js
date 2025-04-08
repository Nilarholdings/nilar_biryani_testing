odoo.define('user_model_access_right.ModelAccessRightFormController', function (require) {
"use strict";

	var FormController = require('web.FormController');

	FormController.include({
		renderButtons: function ($node) {
			var self = this
			self._super.apply(self, arguments)
			if(!self.$buttons) return

			// Hide Create & Edit Button
			self.$buttons.find('.o_form_button_create').hide()
			self.$buttons.find('.o_form_button_edit').hide()
			// Not Allow Quick edit by clicking label & fields
			self.activeActions.edit = false

			self._rpc({
				model: 'hr.employee',
				method: 'check_model_access_right',
				kwargs: {
					model_name: self.modelName
				}
			}).then(function (res) {
				// o_form_buttons_edit  contain Save & Discard
				// o_form_buttons_view  contain Edit & Create
				if (res.can_create) {
					self.$buttons.find('.o_form_button_create').show()
				}
				if (res.can_edit) {
					self.$buttons.find('.o_form_button_edit').show()
					self.activeActions.edit = true
				}
			});

		},
	});
});
