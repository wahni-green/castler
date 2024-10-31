# Copyright (c) 2024, Wahni IT Solutions and contributors
# For license information, please see license.txt

import requests

import frappe
from frappe import _
from frappe.model.document import Document


class CastlerSettings(Document):
	def validate(self):
		if not self.enabled:
			return

		self.validate_castler_settings()

	def validate_castler_settings(self):
		if not self.base_url:
			frappe.throw(_("Please enter Base URL"))

		if not self.api_key:
			frappe.throw(_("Please enter Castler API Key"))

		if not self.api_secret:
			frappe.throw(_("Please enter Castler API Secret"))

		if not self.x_api_key:
			frappe.throw(_("Please enter X-API-Key"))

		response = requests.post(
			f"{self.base_url}/api/v1/auth/api-credential/token",
			headers={
				"X-API-Key": self.x_api_key,
				"Content-Type": "application/json",
			},
			json={
				"apiKey": self.api_key,
				"apiSecret": self.get_password("api_secret"),
			}
		).json()

		if not response.get("success"):
			frappe.throw(str(response))

		self.api_token = response.get("result", {}).get("token")



