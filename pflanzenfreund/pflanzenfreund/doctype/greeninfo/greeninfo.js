// Copyright (c) 2018, libracore and contributors
// For license information, please see license.txt

frappe.ui.form.on('GreenInfo', {
	refresh: function(frm) {
        frm.add_custom_button(__("Sync"), function() 
		{
			sync(frm);
		}).addClass("btn-success");
	}
});

function sync(frm) {
	frappe.call({
		method: 'sync',
		doc: frm.doc,
		callback: function(response) {
			if (response.message) {
				frappe.show_alert(response.message);
			}
		}
	});
}
