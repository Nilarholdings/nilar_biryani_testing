odoo.define('user_model_access_right.ModelAccessRightListController', function (require) {
"use strict";

    var ListController = require('web.ListController');
    ListController.include({
    	init: function (parent, model, renderer, params) {
			this._super.apply(this, arguments);
			this.can_edit_on_line = true;
		},
		// Overwrite
		// Not allow to edit directly on tree view
		_onEditLine: function (ev) {
			var self = this;
			ev.stopPropagation();
			if (this.can_edit_on_line) {
				this.trigger_up('mutexify', {
					action: function () {
						self._setMode('edit', ev.data.recordId)
							.then(ev.data.onSuccess);
					},
				});
			}
		},
		renderButtons: function ($node) {
			var self = this
			self._super.apply(self, arguments)
			if(!self.$buttons) return

			// Hide Create Button
			self.$buttons.find('.o_list_button_add').hide()
			// Hide delete Action Button
			self.activeActions.delete = false
			// Not allow to edit directly on tree view
			self.can_edit_on_line = false

			self._rpc({
				model: 'hr.employee',
				method: 'check_model_access_right',
				kwargs: {
					model_name: self.modelName
				}
			}).then(function (res) {
				if (res.can_create) {
					self.$buttons.find('.o_list_button_add').show()
				}
				if (res.can_edit) {
					self.can_edit_on_line = true
				}
				if (res.can_delete) {
					self.activeActions.delete = true
				}
			});
		},
    });


});
