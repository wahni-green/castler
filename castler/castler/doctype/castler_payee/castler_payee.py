# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from castler.utils import CastlerAPI


class CastlerPayee(Document):
	def before_insert(self):
		self.create_payee()

	def create_payee(self):
		castler_api = CastlerAPI()
		account_details = {
            "account_holder": self.account_holder,
            "email": self.email,
            "mobile": self.mobile,
            "bank": self.bank,
            "bank_address": self.bank_address,
            "account_number": self.account_number,
            "ifsc": self.ifsc,
		}
		escrow_details = castler_api.create_payee(**account_details)

		self.payee_id = escrow_details["payeeId"]
		self.name = self.payee_id
		frappe.msgprint(str(escrow_details))
