# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

import requests

import frappe


class CastlerAPI:
    def __init__(self):
        self.settings = frappe.get_cached_doc("Castler Settings")

    def make_request(self, url, body, method="POST"):
        response = requests.request(
            method,
            url,
            headers={
                "Authorization": f"Bearer {self.settings.get_password('api_token')}",
                "X-API-KEY": self.settings.x_api_key,
                "Content-Type": "application/json",
            },
            json=body
        )
        # response.raise_for_status()
        return response.json()

    def request_b2e_transfer(self, **kwargs):
        # Bank to Escrow Transfer
        url = f"{self.settings.base_url}/api/v1/bank-account/transfer"
        body = {
            "payeeId": kwargs.get("payee_id"),
            "bankAccountNumber": kwargs.get("bank_account_number"),
            "amount": kwargs.get("amount"),
            "customerRefId": kwargs.get("customer_ref_id"),
            "purpose": kwargs.get("purpose"),
            "transferType": kwargs.get("transfer_type"),
        }
        response = self.make_request(url, body)
        if not response.get("success"):
            frappe.throw(
                "<br>".join(response.get("errors", []))
            )
        return response["result"]

    def fetch_b2e_transfer_status(self, transfer_id):
        url = f"{self.settings.base_url}/api/v1/bank-account/transfer/{transfer_id}"
        response = self.make_request(url, {}, "GET")
        if not response.get("success"):
            frappe.throw(
                "<br>".join(response.get("errors", []))
            )
        return response["result"]

    def request_e2e_transfer(self, **kwargs):
        # Escrow to Escrow Transfer
        url = f"{self.settings.base_url}/api/v1/transfer"
        body = {
            "payeeId": kwargs.get("payee_id"),
            "accountId": kwargs.get("escrow_account_id"),
            "amount": kwargs.get("amount"),
            "customerRefId": kwargs.get("customer_ref_id"),
            "purpose": kwargs.get("purpose"),
            "transferType": kwargs.get("transfer_type"),
        }
        response = self.make_request(url, body)
        if not response.get("success"):
            frappe.throw(
                "<br>".join(response.get("errors", []))
            )
        return response["result"]

    def fetch_e2e_transfer_status(self, transfer_id):
        url = f"{self.settings.base_url}/api/v1/transfer/{transfer_id}"
        response = self.make_request(url, {}, "GET")
        if not response.get("success"):
            frappe.throw(
                "<br>".join(response.get("errors", []))
            )
        return response["result"]

    def fetch_bank_balance(self, account_no):
        url = f"{self.settings.base_url}/api/v1/bank-account/{account_no}/balance" 
        response = self.make_request(url, {}, "GET")
        if not response.get("success"):
            frappe.throw(
                "<br>".join(response.get("errors", []))
            )
        return response["result"]
