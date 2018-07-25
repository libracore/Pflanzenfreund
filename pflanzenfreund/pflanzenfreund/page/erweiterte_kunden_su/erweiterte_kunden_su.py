# -*- coding: utf-8 -*-
# Copyright (c) 2017-2018, libracore and contributors
# License: AGPL v3. See LICENCE

from __future__ import unicode_literals
import frappe
from frappe import throw, _

@frappe.whitelist()
def get_all_infos():
	customer_query = """SELECT cus.customer_name, cus.customer_name,  adr.address_line1, adr.pincode, adr.city
		FROM ((`tabAddress` AS adr
		INNER JOIN `tabDynamic Link` AS dyn ON adr.name = dyn.parent)
		INNER JOIN `tabCustomer` AS cus ON dyn.link_name = cus.name)"""
	return frappe.db.sql(customer_query, as_dict=1)
	
@frappe.whitelist()
def get_filtered_infos(name, plz):
	customer_query = """SELECT cus.customer_name, cus.customer_name,  adr.address_line1, adr.pincode, adr.city
		FROM ((`tabAddress` AS adr
		INNER JOIN `tabDynamic Link` AS dyn ON adr.name = dyn.parent)
		INNER JOIN `tabCustomer` AS cus ON dyn.link_name = cus.name)
		WHERE cus.customer_name LIKE '%{0}%'
		AND adr.pincode LIKE '%{1}%'""".format(name, plz)
	return frappe.db.sql(customer_query, as_dict=1)