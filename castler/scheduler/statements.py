# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import add_to_date, get_datetime, now
from castler.utils import CastlerAPI


@frappe.whitelist()
def fetch_statement(account=None):
    frappe.enqueue(
        _fetch_statement,
        queue="long",
        enqueue_after_commit=True,
        account=account
    )
    frappe.msgprint("Statement fetch request has been queued.")


def _fetch_statement(account=None):
    filters = {}
    if account:
        filters["name"] = account

    castler_accounts = frappe.get_all(
        "Castler Account",
        filters=filters,
        fields=["name", "last_sync_on"]
    )
    castler_api = CastlerAPI()

    sync_time = now()

    def get_account_statement(acc):
        statements = []
        is_last_page = False
        page = 1
        while not is_last_page:
            response = castler_api.get_statement(
                acc.name, get_datetime(acc.last_sync_on), sync_time, page
            )
            if not response["result"]:
                break

            statements.extend(response["result"])
            is_last_page = (response["itemsCount"] == response["allItemsCount"])
            page += 1

        return statements

    for account in castler_accounts:
        statements = get_account_statement(account)
        for transaction in statements:
            doc = frappe.new_doc("Castler Statement")
            doc.update({
                "account": account.name,
                "utr": transaction["utr"],
                "status": transaction.get("status") or "N/A",
                "transaction_id": transaction["referenceId"],
                "transaction_created_on": add_to_date(
                    get_datetime(transaction["createdAt"]).replace(tzinfo=None),
                    hours=5,
                    minutes=30
                ),
                "transaction_updated_on": add_to_date(
                    get_datetime(transaction["updatedAt"]).replace(tzinfo=None),
                    hours=5,
                    minutes=30
                ),
                "amount": transaction["amount"],
                "balance": transaction["accountBalance"],
            })

            if transaction.get("beneficiaryAccNumber"):
                doc.update({
                    "transaction_type": "Outward",
                    "bank_account_no": transaction.get("beneficiaryAccNumber"),
                    "bank_account_ifsc": transaction.get("beneficiaryIFSC"),
                    "bank_account_holder": transaction.get("beneficiaryName"),
                    "bank": transaction.get("beneficiaryBankName"),
                })
            elif transaction.get("remitterName"):
                doc.update({
                    "transaction_type": "Inward",
                    "bank_account_no": transaction.get("remitterAccNumber"),
                    "bank_account_ifsc": transaction.get("remitterIFSCCode"),
                    "bank_account_holder": transaction.get("remitterName"),
                })
                
            doc.insert(ignore_permissions=True)

        frappe.db.set_value("Castler Account", account.name, "last_sync_on", sync_time)
