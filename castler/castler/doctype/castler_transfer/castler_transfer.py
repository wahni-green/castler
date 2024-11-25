# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from castler.utils import CastlerAPI


class CastlerTransfer(Document):
	def on_submit(self):
		self.create_transfer()

	def create_transfer(self):
		self.status = "Pending"
		if self.from_type == "Castler Account":
			self.process_e2p_transfer()
		else:
			self.process_b2p_transfer()

	def process_e2p_transfer(self):
		castler_api = CastlerAPI()
		transfer_details = {
			"payee_id": self.to_account,
			"escrow_account_id": self.from_account,
			"amount": self.amount,
			"customer_ref_id": self.name,
			"purpose": self.purpose,
			"transfer_type": self.transfer_type,
		}
		transfer_details = castler_api.request_e2p_transfer(**transfer_details)

		self.transfer_id = transfer_details["transferId"]
		frappe.msgprint(str(transfer_details))

	def process_b2p_transfer(self):
		bank_account_number = frappe.db.get_value("Bank Account", self.to_account, "bank_account_no")
		if not bank_account_number:
			frappe.throw(_("Bank Account Number is required for this transaction"))

		castler_api = CastlerAPI()
		transfer_details = {
			"payee_id": self.to_account,
			"bank_account_number": bank_account_number,
			"amount": self.amount,
			"customer_ref_id": self.name,
			"purpose": self.purpose,
			"transfer_type": self.transfer_type,
		}
		transfer_details = castler_api.request_b2p_transfer(**transfer_details)

		self.transfer_id = transfer_details["transferId"]
		frappe.msgprint(str(transfer_details))
