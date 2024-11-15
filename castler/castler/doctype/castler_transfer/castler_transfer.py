# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from castler.utils import CastlerAPI


class CastlerTransfer(Document):
	def on_submit(self):
		self.create_transfer()

	def create_transfer(self):
		castler_api = CastlerAPI()
		transfer_details = {
			"payee_id": self.to_account,
			"escrow_account_id": self.from_account,
			"amount": self.amount,
			"customer_ref_id": self.name,
			"purpose": self.purpose,
			"transfer_type": self.transfer_type,
		}
		transfer_details = castler_api.request_e2e_transfer(**transfer_details)

		self.transfer_id = transfer_details["transferId"]
		# self.name = self.transfer_id
		self.status = "Pending"
		# msgprint(str(transfer_details))
		frappe.msgprint(str(transfer_details))
