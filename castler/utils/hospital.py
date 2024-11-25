# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import get_datetime


@frappe.whitelist()
def create_hospital_lender_escrow(hospital, email, payee):
    settings = frappe.get_cached_doc("Castler Settings")
    lenders = frappe.db.get_all("Lender", pluck="short_code")
    for lender in lenders:
        escrow = frappe.new_doc("Castler Account")
        escrow.update({
            "account_name": f"{hospital} - {lender}",
            "email": email,
            "start_date": get_datetime(),
            "validity": settings.default_validity or 365,
            "purpose": f"Hospital Lender Escrow: {hospital} - {lender}",
            "expected_volume": settings.default_volume,
            "bank": settings.default_bank,
        })
        escrow.append("payees", {
            "payee": payee,
            "share_type": settings.default_share_type,
            "share": settings.default_share,
        })
        escrow.append("payees", {
            "payee": settings.company_payee,
            "share_type": settings.default_share_type,
            "share": settings.default_share,
        })
        escrow.insert(ignore_permissions=True)
    return True