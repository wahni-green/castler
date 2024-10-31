# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

# import frappe
from frappe import scrub, msgprint, throw
from frappe.utils import get_datetime
from frappe.model.document import Document
from castler.utils import CastlerAPI


class CastlerAccount(Document):
	def before_insert(self):
		self.create_escrow_account()

	def create_escrow_account(self):
		castler_api = CastlerAPI()
		account_details = {
			"email": self.email,
			"account_name": self.account_name,
			"start_date": get_datetime(self.start_date).isoformat(),
			"validity": self.validity,
			"purpose": self.purpose,
			"expected_volume": self.expected_volume,
			"hard_escrow_number": self.hard_escrow_number,
			"bank": scrub(self.bank),
		}
		escrow_details = castler_api.create_escrow_account(**account_details)

		self.account_id = escrow_details["accountId"]
		self.name = self.account_id
		msgprint(str(escrow_details))
