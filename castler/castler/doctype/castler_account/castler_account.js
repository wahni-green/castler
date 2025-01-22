// Copyright (c) 2024, Wahni IT Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("Castler Account", {
	refresh(frm) {
        // add custom button to the form
        frm.add_custom_button('Statement', () => {
            frappe.call("castler.scheduler.statements.fetch_statement");
        }, __("Fetch"));
	},
});
