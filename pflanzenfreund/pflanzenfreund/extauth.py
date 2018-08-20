# -*- coding: utf-8 -*-
# Copyright (c) 2018, libracore and contributors
# For license information, please see license.txt
#
# Call API as
#   /api/method/pflanzenfreund.pflanzenfreund.extauth.check_credentials
#   args { user, password }

import frappe
from frappe.utils.password import check_password

# API function for external authentication
@frappe.whitelist(allow_guest=True)
def check_credentials(user, password):
	if not user or not password:
		frappe.throw("Please provide credentials")
		return { 'status': 'missing credentials' }
	
	user = check_password(user, password)
	if user:
		role = frappe.get_value("User", user, "pflanzenfreund_group")
		return {'status': 'OK', 'user': user, 'role': role}
	return { 'status': 'failed' }
