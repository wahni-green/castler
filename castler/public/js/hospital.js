// Copyright (c) 2024, Wahni IT Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Hospital', {
    refresh: function (frm) {
        frm.add_custom_button(__('Escrow Account'), function () {
            let dialog = new frappe.ui.Dialog({
                title: __("Create Escrow Account"),
                fields: [
                    {
                        fieldname: "email",
                        label: __("Email"),
                        fieldtype: "Data",
                        reqd: 1
                    },
                    {
                        fieldname: "payee",
                        label: __("Payee"),
                        fieldtype: "Link",
                        options: "Castler Account",
                        reqd: 1
                    },
                ],
                primary_action_label: __("Create"),
                primary_action: function () {
                    let values = dialog.get_values();
                    if (!values) return;
                    frappe.call({
                        method: "castler.utils.hospital.create_hospital_lender_escrow",
                        args: {
                            hospital: frm.doc.short_code,
                            email: values.email,
                            payee: values.payee
                        },
                        callback: function (r) {
                            if (r.message) {
                                frappe.msgprint(__("Escrow Accounts created successfully"));
                                dialog.hide();
                            }
                        }
                    });
                }
            });
        }, __("Create"));
    }
});