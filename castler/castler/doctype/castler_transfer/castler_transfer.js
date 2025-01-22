// Copyright (c) 2024, Wahni IT Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on("Castler Transfer", {
    from_account(frm) {
        frm.call('fetch_account_balance');
	},
    from_type(frm) {
        frm.call('fetch_account_balance');
	},
});
